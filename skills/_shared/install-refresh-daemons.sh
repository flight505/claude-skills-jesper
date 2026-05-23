#!/usr/bin/env bash
# Install launchd daemons that weekly-refresh every doc-skill in this repo.
#
# Convention: any skill at skills/<name>/ with scripts/update-*.sh is treated
# as a refreshable doc-skill. The installer generates one plist per skill with
# the clone's working-tree path baked in, so this works on any machine where
# the repo lives.
#
# Usage:
#   skills/_shared/install-refresh-daemons.sh              # install missing
#   skills/_shared/install-refresh-daemons.sh --force      # rewrite existing
#   skills/_shared/install-refresh-daemons.sh --uninstall  # tear down all
#   skills/_shared/install-refresh-daemons.sh --list       # show what would land
#
# Schedule: Sundays 04:00 local. RunAtLoad=true on first install so a fresh
# clone has fresh docs within seconds.

set -euo pipefail

LABEL_PREFIX="com.flight505"
SCHEDULE_WEEKDAY=0  # 0 = Sunday
SCHEDULE_HOUR=4
SCHEDULE_MINUTE=0

# Resolve repo root from this script's location.
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
LAUNCH_AGENTS="$HOME/Library/LaunchAgents"
LOG_DIR="$HOME/.local/var/log"

[[ "$(uname)" == "Darwin" ]] || {
  echo "error: macOS only (uses launchd). Linux/Windows users: set up cron/Task Scheduler manually using the commands printed by --list." >&2
  exit 1
}

mode="install"
force=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --force)     force=1; shift;;
    --uninstall) mode="uninstall"; shift;;
    --list)      mode="list"; shift;;
    -h|--help)   sed -n '2,16p' "$0"; exit 0;;
    *)           echo "unknown arg: $1" >&2; exit 2;;
  esac
done

# Discover doc-skills: any skill dir with at least one scripts/update-*.sh.
# Outputs "<name>|<comma-separated-script-basenames>" per skill, lex-sorted.
discover_skills() {
  for skill_dir in "$REPO_ROOT/skills/"*/; do
    [[ -d "${skill_dir}scripts" ]] || continue
    scripts=()
    for s in "${skill_dir}scripts/update-"*.sh; do
      [[ -f "$s" ]] && scripts+=("$(basename "$s")")
    done
    [[ ${#scripts[@]} -gt 0 ]] || continue
    name="$(basename "$skill_dir")"
    IFS=','; echo "${name}|${scripts[*]}"; unset IFS
  done | sort
}

label_for() {
  # Strip "-skill" suffix if present. Keeps labels readable and matches the
  # convention used by the pre-existing plists on the maintainer's machine.
  echo "${1%-skill}"
}

emit_plist() {
  local name="$1" scripts_csv="$2" plist="$3"
  local short; short="$(label_for "$name")"
  # Build chained bash command: cd <dir> && bash scripts/a.sh && bash scripts/b.sh
  local cmd="cd '$REPO_ROOT/skills/${name}'"
  IFS=','; for s in $scripts_csv; do
    cmd="${cmd} && bash scripts/${s}"
  done; unset IFS

  cat > "$plist" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>${LABEL_PREFIX}.${short}-refresh</string>

    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>-c</string>
        <string>${cmd}</string>
    </array>

    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>${HOME}/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin</string>
        <key>HOME</key>
        <string>${HOME}</string>
    </dict>

    <key>StartCalendarInterval</key>
    <dict>
        <key>Weekday</key>
        <integer>${SCHEDULE_WEEKDAY}</integer>
        <key>Hour</key>
        <integer>${SCHEDULE_HOUR}</integer>
        <key>Minute</key>
        <integer>${SCHEDULE_MINUTE}</integer>
    </dict>

    <key>RunAtLoad</key>
    <true/>

    <key>StandardOutPath</key>
    <string>${LOG_DIR}/${name}-refresh.log</string>
    <key>StandardErrorPath</key>
    <string>${LOG_DIR}/${name}-refresh.log</string>
</dict>
</plist>
PLIST
}

case "$mode" in
  list)
    echo "would install (Weekday=Sun, $SCHEDULE_HOUR:0$SCHEDULE_MINUTE local, RunAtLoad=true):"
    while IFS='|' read -r name scripts_csv; do
      echo "  ${LABEL_PREFIX}.$(label_for "$name")-refresh"
      IFS=','; for s in $scripts_csv; do echo "    \$ bash skills/${name}/scripts/${s}"; done; unset IFS
    done < <(discover_skills)
    exit 0;;

  uninstall)
    while IFS='|' read -r name _; do
      plist="${LAUNCH_AGENTS}/${LABEL_PREFIX}.$(label_for "$name")-refresh.plist"
      if [[ -f "$plist" ]]; then
        launchctl bootout "gui/$UID" "$plist" 2>/dev/null || true
        rm -f "$plist"
        echo "[uninstall] $name"
      fi
    done < <(discover_skills)
    exit 0;;

  install)
    mkdir -p "$LAUNCH_AGENTS" "$LOG_DIR"
    installed=0; skipped=0
    while IFS='|' read -r name scripts_csv; do
      plist="${LAUNCH_AGENTS}/${LABEL_PREFIX}.$(label_for "$name")-refresh.plist"
      if [[ -f "$plist" ]] && [[ $force -eq 0 ]]; then
        echo "[skip] $name (plist exists; pass --force to reinstall)"
        ((skipped++)) || true
        continue
      fi
      # If reinstalling, unload first so launchctl picks up the new plist.
      [[ -f "$plist" ]] && launchctl bootout "gui/$UID" "$plist" 2>/dev/null || true
      emit_plist "$name" "$scripts_csv" "$plist"
      if launchctl bootstrap "gui/$UID" "$plist" 2>/dev/null; then
        echo "[install] $name -> $plist (fires immediately + Sundays $SCHEDULE_HOUR:0$SCHEDULE_MINUTE)"
        ((installed++)) || true
      else
        echo "warn: launchctl bootstrap failed for $name (plist written but not loaded)" >&2
      fi
    done < <(discover_skills)
    echo
    echo "summary: $installed installed, $skipped skipped"
    [[ $installed -gt 0 ]] && echo "logs: $LOG_DIR/<skill>-refresh.log"
    exit 0;;
esac
