# Linux / DGX Spark Install Guide

This marketplace was authored on macOS and is personal-first, but everything
except the doc-refresh daemons works on Linux. This page covers the gaps.

## What works out of the box

| Component | Status |
|---|---|
| `forge` TUI + CLI | ✅ pure Go, cross-platform |
| `forge serve` (web UI) | ✅ pure Go + embedded SPA |
| `forge suggest --project` | ✅ reads files, runs `git log` |
| Chat (TUI `c` key / web) | ✅ auth via env vars (no Keychain needed) |
| `scripts/regenerate-marketplace.py` | ✅ Python stdlib |
| `scripts/sync-upstream.sh` | ✅ uses `git` |
| `scripts/check-sources.py` | ✅ Python stdlib + `git` |
| `scripts/check-sources.py --fix` (docs) | ⚠️ needs cron wired up first (see below) |
| `scripts/check-sources.py --fix` (subtree) | ✅ calls sync-upstream.sh |
| `skills/_shared/install-refresh-daemons.sh` | ❌ macOS/launchd only |

## Install forge

### Option A — build from source (recommended)

```bash
git clone https://github.com/flight505/forge
cd forge
make build       # requires Go ≥ 1.23
make install     # copies binary to ~/.local/bin/forge
```

### Option B — go install

```bash
go install github.com/flight505/forge/cmd/forge@latest
```

The binary ends up in `$GOPATH/bin` or `~/go/bin`. Add to `$PATH` if needed.

## Set up auth (no macOS Keychain on Linux)

The macOS Keychain probe is already darwin-gated in forge — it's a no-op on
Linux. Set one of these env vars instead:

```bash
# Preferred for Claude Max (matches Claude Code CLI's own env var):
export CLAUDE_CODE_OAUTH_TOKEN="sk-ant-oat01-..."

# Alternative (canonical Anthropic SDK env var):
export ANTHROPIC_AUTH_TOKEN="sk-ant-oat01-..."

# Or a standalone API key:
export ANTHROPIC_API_KEY="sk-ant-api01-..."
```

Add to `~/.bashrc` / `~/.zshrc` so it persists.

## Doc-skill refresh — replace launchd with cron

`skills/_shared/install-refresh-daemons.sh` is macOS-only (uses
`launchd` + `~/Library/LaunchAgents`). On Linux, set up cron manually.

### Step 1 — see what commands would fire

```bash
skills/_shared/install-refresh-daemons.sh --list
```

Example output:
```
  com.flight505.claude-docs-refresh
    $ bash skills/claude-docs-skill/scripts/update-cli-docs.sh
    $ bash skills/claude-docs-skill/scripts/update-llms.sh
  com.flight505.openrouter-docs-refresh
    $ bash skills/openrouter-docs-skill/scripts/update-openrouter-docs.sh
  ...
```

### Step 2 — add cron entries

```bash
crontab -e
```

Add a weekly Sunday 04:00 entry per doc-skill. Substitute the full path
to the repo root for `REPO`:

```cron
# forge doc-skill refresh — Sunday 04:00 weekly
REPO=/path/to/claude-skills-jesper
PATH=/usr/local/bin:/usr/bin:/bin
0 4 * * 0  cd "$REPO/skills/claude-docs-skill"    && bash scripts/update-cli-docs.sh && bash scripts/update-llms.sh
0 4 * * 0  cd "$REPO/skills/openrouter-docs-skill" && bash scripts/update-openrouter-docs.sh
0 4 * * 0  cd "$REPO/skills/warp-docs-skill"       && bash scripts/update-docs.sh
0 4 * * 0  cd "$REPO/skills/gemini-docs-skill"     && bash scripts/update-docs.sh
0 4 * * 0  cd "$REPO/skills/spark-docs-skill"      && bash scripts/update-docs.sh
0 4 * * 0  cd "$REPO/skills/nvidia-dgx-research"   && bash scripts/update-catalog.sh
0 4 * * 0  cd "$REPO/skills/design-md"             && bash scripts/update-templates.sh
```

### Step 3 — trigger an immediate first refresh

After setting up cron, run the scripts once so references/ dirs aren't empty:

```bash
cd /path/to/claude-skills-jesper
for sk in skills/claude-docs-skill skills/openrouter-docs-skill skills/warp-docs-skill \
          skills/gemini-docs-skill skills/spark-docs-skill skills/nvidia-dgx-research \
          skills/design-md; do
  pushd "$sk" >/dev/null
  for s in scripts/update-*.sh; do [ -f "$s" ] && bash "$s"; done
  popd >/dev/null
done
```

Or use the check-sources script to find and fix stale items:

```bash
python3 scripts/check-sources.py --no-color
# For each STALE item printed, run its update script manually
```

### Alternative — systemd timer

If you prefer systemd over cron:

```bash
mkdir -p ~/.config/systemd/user

cat > ~/.config/systemd/user/forge-docs-refresh.service <<'EOF'
[Unit]
Description=forge doc-skill weekly refresh

[Service]
Type=oneshot
WorkingDirectory=/path/to/claude-skills-jesper
ExecStart=/bin/bash -c 'for sk in skills/*/scripts/update-*.sh; do bash "$sk" || true; done'
StandardOutput=append:/tmp/forge-docs-refresh.log
StandardError=append:/tmp/forge-docs-refresh.log
EOF

cat > ~/.config/systemd/user/forge-docs-refresh.timer <<'EOF'
[Unit]
Description=forge doc-skill weekly refresh timer

[Timer]
OnCalendar=Sun *-*-* 04:00:00
Persistent=true

[Install]
WantedBy=timers.target
EOF

systemctl --user daemon-reload
systemctl --user enable --now forge-docs-refresh.timer
```

## Open-URL (`o` key) on headless Linux

On a headless DGX Spark accessed over SSH, `xdg-open` may not work.
The `o` key in the TUI will fail silently (forge calls `xdg-open`, it
exits non-zero, a toast shows the error). Not a blocking issue — copy
the URL from the preview pane manually instead.

To set up `xdg-open` on a desktop Linux: install `xdg-utils`.

## `trash` command

Some workflow scripts and session notes use `trash` (Homebrew-installed
macOS utility). On Linux, substitute `rm -rf` or install `trash-cli`:

```bash
pip install trash-cli      # provides `trash` command
# or: sudo apt install trash-cli
```

## Summary checklist for DGX Spark / headless Linux

- [ ] Clone repo + build/install forge binary
- [ ] Export `CLAUDE_CODE_OAUTH_TOKEN` (or `ANTHROPIC_API_KEY`) in shell profile
- [ ] Add cron entries (or systemd timer) for weekly doc-skill refresh
- [ ] Run first refresh manually: `for sk in skills/*/scripts/update-*.sh; do bash "$sk" || true; done`
- [ ] `python3 scripts/check-sources.py --no-color` — all docs should show "OK"
- [ ] `forge agent search test` — verify catalog loads
- [ ] Restart Claude Code session to pick up newly installed skills/agents
