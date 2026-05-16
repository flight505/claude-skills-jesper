# Warp Terminal Documentation Index

Organized reference for finding topics.
Use grep on `full-docs.txt` for full content.

## Sections Overview

| Section | Pages | Description |
|---------|-------|-------------|
| [CODE](#code) | 9 | Code editing, review, and codebase context features |
| [GETTING-STARTED](#getting-started) | 14 | Installation, setup, keyboard shortcuts, and shell configuration |
| [HOME](#home) | 1 | Documentation section |
| [KNOWLEDGE-AND-COLLABORATION](#knowledge-and-collaboration) | 11 | Warp Drive, notebooks, workflows, teams, and sharing |
| [TERMINAL](#terminal) | 69 | Terminal features: blocks, input, output, tabs, themes, and more |

════════════════════════════════════════════════════════════════════════════════
## CODE
*Code editing, review, and codebase context features*

**9 pages in this section:**

### Built-in code editor
**Path:** `/code/code-editor`
**Summary:** Warp comes with a native code editor designed for quick, in-flow edits alongside your Agent conversations. Instead of switching back and forth to an IDE, you can open and edit files directly in War...

### Code editor Vim keybindings
**Path:** `/code/code-editor/code-editor-vim-keybindings`
**Summary:** The Vi family of programs (including Vim and Neovim) are modal text editors that allow for keyboard-driven text editing. Vi-style keybindings are especially popular among developers for their speed...

### File Tree (Project Explorer)
**Path:** `/code/code-editor/file-tree`
**Summary:** <figure><img src="https://4009768362-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FPsjNxoJ0NFCXW6rRdHH3%2Fuploads%2Fgit-blob-39320c4ee515f98d017a80234b2643627e73ca10%2Ffiletre...

### Find & replace
**Path:** `/code/code-editor/find-and-replace`
**Summary:** Press `CMD-F` on macOS or `CTRL-SHIFT-F` on Windows and Linux to open the find menu. As you type, all matches in the file are highlighted, and the match closest to your cursor is selected.

### Language Server Protocol (LSP)
**Path:** `/code/code-editor/language-server-protocol`
**Summary:** Warp's code editor includes built-in support for the [Language Server Protocol](https://microsoft.github.io/language-server-protocol/), giving you IDE-grade code intelligence directly in the termin...

### Code Review panel
**Path:** `/code/code-review`
**Summary:** When you are working locally in a Git repository with uncommitted changes, the **Code Review panel** lets you inspect, edit, and manage code changes directly inside Warp. It integrates with Git and...

### Git Worktrees
**Path:** `/code/git-worktrees`
**Summary:** Warp natively supports [Git worktrees](https://git-scm.com/docs/git-worktree) — a Git feature that lets you check out multiple branches simultaneously in separate directories, all backed by the sam...

### Code overview
**Path:** `/code/overview`
**Summary:** {% hint style="info" %} Several coding features — including Codebase Context, code diffs, the code editor, and the file tree — are not yet available in SSH or WSL sessions. {% endhint %}

### Feature support over SSH
**Path:** `/code/ssh-feature-support`
**Summary:** When you [Warpify an SSH session](https://docs.warp.dev/terminal/warpify/ssh), Warp's core terminal features — the input editor, completions, blocks, history search, and more — work the same as the...


════════════════════════════════════════════════════════════════════════════════
## GETTING-STARTED
*Installation, setup, keyboard shortcuts, and shell configuration*

**14 pages in this section:**

### Coding in Warp
**Path:** `/getting-started/coding-in-warp`
**Summary:** When you enter a Git repo for the first time, Warp will enter an initialization flow to index your codebase and generate an AGENTS.md file.

### Customizing Warp
**Path:** `/getting-started/customizing-warp`
**Summary:** Warp is deeply customizable. Whether you use Warp primarily as a modern terminal or as an AI-powered development environment, you can tailor the experience to fit how you work. Configure the termin...

### Installation and setup
**Path:** `/getting-started/installation-and-setup`
**Summary:** {% hint style="info" %} **Platform support:** Warp is supported on macOS (Intel and Apple silicon), Windows (x86\_64 and ARM64), and Linux (x86\_64 and ARM64). {% endhint %}

### Keyboard shortcuts
**Path:** `/getting-started/keyboard-shortcuts`
**Summary:** Warp opens with a shortcut screen showing some of the most commonly used keyboard shortcuts. Hide the shortcut screen by clicking the x button. Quickly view keyboard shortcuts via the [Command Pale...

### Migrate to Warp
**Path:** `/getting-started/migrate-to-warp`
**Summary:** Warp users come from every kind of terminal, editor, and AI coding tool. This section has a dedicated page for each of the most common sources, with step-by-step migration guidance, notes on what t...

### Migrate to Warp from Claude Code
**Path:** `/getting-started/migrate-to-warp/migrate-to-warp-from-claude-code`
**Summary:** Claude Code is different from the other sources in this section: it's not a terminal emulator, it's a CLI agent that runs inside any terminal. Warp is an agentic development environment with a buil...

### Migrate to Warp from Cursor
**Path:** `/getting-started/migrate-to-warp/migrate-to-warp-from-cursor`
**Summary:** Warp gives Cursor users two clean migration paths: keep Cursor as your editor and use Warp for terminal and agent work, or move fully to Warp's built-in code editor and Agent Mode. This page walks ...

### Migrate to Warp from Ghostty
**Path:** `/getting-started/migrate-to-warp/migrate-to-warp-from-ghostty`
**Summary:** Warp gives Ghostty users a fast path to bring over themes, fonts, and keybindings — plus native equivalents for the Ghostty features you rely on, from the quick terminal to native tabs and splits.

### Migrate to Warp from iTerm2
**Path:** `/getting-started/migrate-to-warp/migrate-to-warp-from-iterm2`
**Summary:** Warp imports your iTerm2 profile automatically, bringing over theme, font, keybindings, hotkey window, and more in a few clicks. This page walks through the importer, what it covers, and what to re...

### Migrate to Warp from macOS Terminal
**Path:** `/getting-started/migrate-to-warp/migrate-to-warp-from-macos-terminal`
**Summary:** Warp gives Terminal.app users everything they already have — shell, theme, font, prompt — plus split panes, tabs, blocks, and Agent Mode for an AI-assisted workflow. This page walks through both an...

### Migrate to Warp from VS Code terminal
**Path:** `/getting-started/migrate-to-warp/migrate-to-warp-from-vs-code-terminal`
**Summary:** Warp lets VS Code users choose their own path: keep VS Code for editing and run Warp as the terminal alongside it, or replace both with Warp's built-in code editor. This page walks through reconfig...

### Migrate to Warp from Windows Terminal
**Path:** `/getting-started/migrate-to-warp/migrate-to-warp-from-windows-terminal`
**Summary:** Warp on Windows covers everything you use Windows Terminal for today — profiles, PowerShell, color schemes, keybindings — with Agent Mode and blocks on top. This page walks through the migration.

### Warp quickstart
**Path:** `/getting-started/quickstart`
**Summary:** This guide walks you through installing Warp, trying the terminal features you'll use every day, and firing off your first agent prompt. After completing the steps in this guide, you'll have a work...

### Supported shells
**Path:** `/getting-started/supported-shells`
**Summary:** Warp tries to load your login shell by default. Currently, Warp supports bash, fish, zsh, and PowerShell (pwsh). If your login shell is set to something else (e.g. Nushell) Warp will show a banner ...


════════════════════════════════════════════════════════════════════════════════
## HOME

**1 pages in this section:**

### <!DOCTYPE html><html data-dpl-id="p-0e10124626d53231da96a582439ff0" lang="en" cl
**Path:** `/`


════════════════════════════════════════════════════════════════════════════════
## KNOWLEDGE-AND-COLLABORATION
*Warp Drive, notebooks, workflows, teams, and sharing*

**11 pages in this section:**

### Team Admin Panel
**Path:** `/knowledge-and-collaboration/admin-panel`
**Summary:** The [Admin Panel](https://app.warp.dev/admin/) provides team administrators with centralized control over organization-wide settings in Warp. It allows you to manage workspace settings that are enf...

### Session sharing
**Path:** `/knowledge-and-collaboration/session-sharing`
**Summary:** Session sharing documentation has moved to the Agent Platform section. See the articles below for details on sharing sessions:

### Team management
**Path:** `/knowledge-and-collaboration/teams`
**Summary:** A team is a group of Warp users who can collaborate on the command line together. Warp teams can share a dedicated workspace in Warp Drive. [Learn about pricing](https://www.warp.dev/pricing) and s...

### Warp Drive overview
**Path:** `/knowledge-and-collaboration/warp-drive`
**Summary:** All objects stored in Warp Drive sync immediately as they’re updated, so you and your team will always have access to the latest versions.

### Agent Mode context
**Path:** `/knowledge-and-collaboration/warp-drive/agent-mode-context`
**Summary:** [Agent Mode](https://docs.warp.dev/agent-platform/warp-agents/interacting-with-agents) can leverage your [Warp Drive](https://docs.warp.dev/knowledge-and-collaboration/warp-drive) contents to tailo...

### AI-Integrated Objects
**Path:** `/knowledge-and-collaboration/warp-drive/ai-objects`
**Summary:** Warp Drive includes several object types that integrate with Warp's agents to provide personalized, context-aware assistance. These objects help agents understand your coding standards, connect to ...

### Environment variables
**Path:** `/knowledge-and-collaboration/warp-drive/environment-variables`
**Summary:** Environment variables in Warp are similar to .env files, except you can:

### Warp Drive Notebooks
**Path:** `/knowledge-and-collaboration/warp-drive/notebooks`
**Summary:** Notebooks are runnable documentation consisting of markdown text and list elements, code blocks, and runnable shell snippets that can be automatically executed in your terminal session. Notebooks a...

### Warp Drive prompts
**Path:** `/knowledge-and-collaboration/warp-drive/prompts`
**Summary:** A prompt is a parameterized natural language query you can name and save in Warp to use with [Agent Mode](https://docs.warp.dev/agent-platform/warp-agents/interacting-with-agents).

### Warp Drive on the web
**Path:** `/knowledge-and-collaboration/warp-drive/web`
**Summary:** Warp Drive on the Web lets you view and edit your Warp Drive objects and shared sessions directly in the browser, on any device.

### Warp Drive Workflows
**Path:** `/knowledge-and-collaboration/warp-drive/workflows`
**Summary:** A workflow is a parameterized command you can name and save in Warp with descriptions and arguments. Workflows are searchable and easily accessed from the [Command Palette](https://docs.warp.dev/te...


════════════════════════════════════════════════════════════════════════════════
## TERMINAL
*Terminal features: blocks, input, output, tabs, themes, and more*

**69 pages in this section:**

### Terminal appearance
**Path:** `/terminal/appearance`
**Summary:** - [Terminal themes](https://docs.warp.dev/terminal/appearance/themes.md): Warp includes several themes (out-of-box) and also supports setting custom themes. - [Custom themes](https://docs.warp.dev/...

### Custom app icons
**Path:** `/terminal/appearance/app-icons`
**Summary:** {% hint style="info" %} App icons are only available for Warp on macOS. The feature doesn't support custom dock icons. {% endhint %}

### Blocks behavior
**Path:** `/terminal/appearance/blocks-behavior`
**Summary:** Warp offers the option to enable Compact mode, which condenses the spacing between [Blocks](https://docs.warp.dev/terminal/blocks), enabling more content to be in view.

### Custom themes
**Path:** `/terminal/appearance/custom-themes`
**Summary:** {% hint style="info" %} Examples and a collection of themes can be found in the [Warp themes repository](https://github.com/warpdotdev/themes). {% endhint %}

### Input position
**Path:** `/terminal/appearance/input-position`
**Summary:** You can select from three different input positions, which each have different modes of behavior for the flow of input/output Blocks.

### Pane dimming & focus
**Path:** `/terminal/appearance/pane-dimming`
**Summary:** The panes that aren't active will be dimmed to better indicate which pane is active. To access it, go to **Settings** > **Appearance** > **Panes**

### Terminal prompt
**Path:** `/terminal/appearance/prompt`
**Summary:** Warp supports two prompt types: the **Warp prompt** and the **Shell prompt (PS1)**.

### Size, opacity, & blurring
**Path:** `/terminal/appearance/size-opacity-blurring`
**Summary:** To access size settings, go to **Settings** > **Appearance** > **Window**.

### Tabs behavior
**Path:** `/terminal/appearance/tabs-behavior`
**Summary:** Tab indicators provide visual cues in the tab bar under certain specific conditions: When the current pane is maximized, when panes or tabs are synchronized, and when a command exits with an error....

### Text, fonts, & cursor
**Path:** `/terminal/appearance/text-fonts-cursor`
**Summary:** {% hint style="info" %} Once a new font is installed in your system, you need to restart Warp for it to show on the list of options. You may also need to check "View all available system fonts" to ...

### Terminal themes
**Path:** `/terminal/appearance/themes`
**Summary:** The Theme Picker can be accessed by:

### Terminal Blocks
**Path:** `/terminal/blocks`
**Summary:** Blocks enable us to easily:

### Background blocks
**Path:** `/terminal/blocks/background-blocks`
**Summary:** Commands can start background processes that continue even after they exit. You can also start a background process directly from the shell, such as by running it with `&`.

### Block actions
**Path:** `/terminal/blocks/block-actions`
**Summary:** There are 2 ways you can access Block actions.

### Terminal Block basics
**Path:** `/terminal/blocks/block-basics`
**Summary:** * Blocks group your command and command output * The Input Editor can pin to the bottom, pin to the top, or start at the top. * Blocks grow from the bottom to the top. * Blocks are color-coded. Blo...

### Block filtering
**Path:** `/terminal/blocks/block-filtering`
**Summary:** Filter the output lines of a block in Warp to quickly focus on a subset of the block. You can filter by plaintext, regex, invert, or make your filter case-sensitive. You can also add context lines ...

### Block sharing
**Path:** `/terminal/blocks/block-sharing`
**Summary:** {% hint style="info" %} This action sends command information to our server and is explicitly opt-in. Read more about privacy at Warp on [our privacy page](https://www.warp.dev/privacy). {% endhint %}

### Terminal Block find
**Path:** `/terminal/blocks/find`
**Summary:** Find searches for matches in all your Blocks from the bottom up and can even be isolated to a specific Block.

### Sticky Command Header
**Path:** `/terminal/blocks/sticky-command-header`
**Summary:** {% hint style="info" %} For long-running commands that take up the full screen, the sticky header only shows after you start scrolling up. This is to prevent the header from blocking the top part o...

### Classic Input
**Path:** `/terminal/classic-input`
**Summary:** Classic Input corresponds to the **Shell (PS1)** option under **Settings** > **Appearance** > **Input**. It provides a traditional terminal experience with support for shell customizations like PS1...

### Command completions
**Path:** `/terminal/command-completions`
**Summary:** 1. [Completions](https://docs.warp.dev/terminal/command-completions/completions) will suggest commands, option names, and path parameters for you. 2. [Autosuggestions](https://docs.warp.dev/termina...

### Autosuggestions
**Path:** `/terminal/command-completions/autosuggestions`
**Summary:** * From the [Command Palette](https://docs.warp.dev/terminal/command-palette), type in "Autosuggestions" to toggle.

### Tab completions
**Path:** `/terminal/command-completions/completions`
**Summary:** Completions feature fuzzy search capability that provides you with [approximate matches](https://en.wikipedia.org/wiki/Approximate_string_matching) for your queries. If you're unsure about the exac...

### Command Palette
**Path:** `/terminal/command-palette`
**Summary:** <figure><img src="https://4009768362-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FPsjNxoJ0NFCXW6rRdHH3%2Fuploads%2Fgit-blob-4c11592c5193014fb17df1dbdbd8670a118234f3%2Fcommand...

### Terminal comparisons
**Path:** `/terminal/comparisons`
**Summary:** Warp is a modern terminal built in Rust with GPU rendering, agent support, and a code-editor-style input. Use this section to see how Warp stacks up against other popular terminals on raw performan...

### Performance benchmarks
**Path:** `/terminal/comparisons/performance`
**Summary:** We chose to benchmark Warp against 4 other terminal emulator applications, based on their popularity as well as language and principles. Here is the list of the applications we chose for this compa...

### Modern text editing
**Path:** `/terminal/editor`
**Summary:** {% hint style="info" %} Text Editor Input also works for [SSH sessions](https://docs.warp.dev/terminal/warpify/ssh). {% endhint %}

### Alias expansion
**Path:** `/terminal/editor/alias-expansion`
**Summary:** {% tabs %} {% tab title="macOS" %} When Alias Expansion is enabled, type an alias and then hit `SPACE` will expand the alias.

### Command inspector
**Path:** `/terminal/editor/command-inspector`
**Summary:** {% tabs %} {% tab title="macOS" %} Hover over the part of the command you want to inspect with your mouse or press `CMD-SHIFT-I` to inspect the cursor's current location. {% endtab %}

### Syntax & error highlighting
**Path:** `/terminal/editor/syntax-error-highlighting`
**Summary:** Warp supports Syntax Highlighting in the [Input Editor.](https://docs.warp.dev/terminal/editor) It colors each part of a command to help differentiate between sub-commands, options/flags, arguments...

### Input editor Vim keybindings
**Path:** `/terminal/editor/vim`
**Summary:** The Vi family of programs (including Vim and Neovim) are modal text editors that allow for keyboard-driven text editing. Several shells, including `bash` and `zsh`, implement vi-style keybindings. ...

### Command entry
**Path:** `/terminal/entry`
**Summary:** 1. [Command Corrections](https://docs.warp.dev/terminal/entry/command-corrections) provides auto-correct suggestions on previously run commands to catch typos, and forgotten flags, and fix general ...

### Command corrections
**Path:** `/terminal/entry/command-corrections`
**Summary:** This feature was built on top of the open-source project [nvdn/thefuck](https://github.com/nvbn/thefuck). Here are some examples that the Warp team usually finds Command Corrections useful for:

### Command history
**Path:** `/terminal/entry/command-history`
**Summary:** While running, Warp isolates the history of each shell session e.g. if you have two Split Panes open, commands created in one pane do not populate the history of the other. Warp combines the histor...

### Command search
**Path:** `/terminal/entry/command-search`
**Summary:** The Command Search panel provides unified search across all your terminal inputs, saved commands, and [Terminal and Agent modes](https://docs.warp.dev/agent-platform/warp-agents/interacting-with-ag...

### Synchronized inputs
**Path:** `/terminal/entry/synchronized-inputs`
**Summary:** Synchronized inputs in Warp work similarly to “broadcast input” settings in other terminals, but there are some differences.

### YAML workflows
**Path:** `/terminal/entry/yaml-workflows`
**Summary:** {% hint style="danger" %} You can continue to use YAML-based workflows, but we recommend using new [workflows in Warp Drive](https://docs.warp.dev/knowledge-and-collaboration/warp-drive/workflows) ...

### Terminal integrations
**Path:** `/terminal/integrations-and-plugins`
**Summary:** {% hint style="info" %} Currently, the Docker extension is only available on macOS. {% endhint %}

### More Features
**Path:** `/terminal/more-features`
**Summary:** - [Accessibility](https://docs.warp.dev/terminal/more-features/accessibility.md): Warp's accessibility features include VoiceOver support, voice input, and configurable verbosity. - [Files, links, ...

### Accessibility
**Path:** `/terminal/more-features/accessibility`
**Summary:** {% hint style="info" %} Note that currently, these instructions are for macOS only. Warp doesn't support screen readers on Linux or Windows and it's being tracked here: <https://github.com/warpdotd...

### Audible terminal bell
**Path:** `/terminal/more-features/audible-bell`
**Summary:** Warp allows you to enable an audible terminal bell (disabled by default) that can be triggered by a variety of CLI tools (for example, `ping -a`).

### Files, links, & scripts
**Path:** `/terminal/more-features/files-and-links`
**Summary:** Warp supports opening files, folders, and URL links that are within Blocks. Multiple URL protocols are supported e.g. `https`, `ftp`, `file`, etc. Warp can open files and folders in a variety of ed...

### Full-screen apps
**Path:** `/terminal/more-features/full-screen-apps`
**Summary:** Warp supports configuring how to handle mouse and scroll events. They can be sent to the currently running app, e.g. `vim`, or kept and handled by Warp.

### Warp for Linux
**Path:** `/terminal/more-features/linux`
**Summary:** Warp Wayland support can be enabled in **Settings** > **Features** > **System**. Enabling Wayland support may fix issues with blurry text if you have fractional scaling enabled in your window manager.

### Markdown viewer
**Path:** `/terminal/more-features/markdown-viewer`
**Summary:** Warp can be used for both editing and viewing rendered Markdown files in a [split pane](https://docs.warp.dev/terminal/windows/split-panes). Any local file with the `.md` or `.markdown` extension i...

### Desktop notifications
**Path:** `/terminal/more-features/notifications`
**Summary:** Notifications can be sent when a command completes after a configurable number of seconds or when a running command needs you to enter a password to proceed. For either of these triggers, Warp will...

### Terminal quit warning
**Path:** `/terminal/more-features/quit-warning`
**Summary:** The quit warning feature ensures that you receive a warning before quitting the app with a running process, allowing you to save your work and avoid any unintended data loss.\ If you quit the app o...

### Settings Sync (Beta)
**Path:** `/terminal/more-features/settings-sync`
**Summary:** * You can toggle Settings Sync within the **Settings** > **Account** pane * Through the [Command Palette](https://docs.warp.dev/terminal/command-palette) by searching for “Settings Sync”

### Text selection
**Path:** `/terminal/more-features/text-selection`
**Summary:** **Smart selection** goes beyond the typical double-click selection, which only highlights a single word. Instead, it uses semantic rules to treat common patterns (like URLs or file paths) as one un...

### Warp URI scheme
**Path:** `/terminal/more-features/uri-scheme`
**Summary:** There are several ways to use the URI scheme:

### Working directory
**Path:** `/terminal/more-features/working-directory`
**Summary:** Warp's working directory feature is designed to enhance your workflow by enabling you to set up a default directory for new sessions. This feature helps you save time and quickly access your prefer...

### Sessions
**Path:** `/terminal/sessions`
**Summary:** 1. [Session Navigation](https://docs.warp.dev/terminal/sessions/session-navigation) enables you to easily navigate to any session in Warp. 2. [Session Restoration](https://docs.warp.dev/terminal/se...

### Session navigation
**Path:** `/terminal/sessions/session-navigation`
**Summary:** 1. Open the Session Navigation palette with the [Command Palette](https://docs.warp.dev/terminal/command-palette), click on **session >\_** or type in "sessions:". 2. Jump to a session by using you...

### Session restoration
**Path:** `/terminal/sessions/session-restoration`
**Summary:** Session restoration allows you to quickly pick up where you left off in your previous terminal session.

### Settings file
**Path:** `/terminal/settings`
**Summary:** Warp stores your preferences in a plain-text file called `settings.toml`. You can edit it directly in any text editor, check it into version control, or generate it with a script. Changes take effe...

### All settings reference
**Path:** `/terminal/settings/all-settings`
**Summary:** This page lists every setting you can configure in [`settings.toml`](https://docs.warp.dev/terminal/settings) organized by TOML section. For an introduction to the settings file, how to open it, an...

### Terminal features
**Path:** `/terminal/terminal-features`
**Summary:** To make it more transparent & useful, we also show the results for 4 other popular macOS terminal emulators.

### Warpify overview
**Path:** `/terminal/warpify`
**Summary:** 1. [Subshells](https://docs.warp.dev/terminal/warpify/subshells), Warp supports enabling Warp features in subshells for bash, zsh, and fish. 2. [SSH](https://docs.warp.dev/terminal/warpify/ssh), Wa...

### SSH with Warp features
**Path:** `/terminal/warpify/ssh`
**Summary:** {% hint style="info" %} Some coding features — including Codebase Context, code diffs, the code editor, and the file tree — are not yet available over SSH. See [Feature support over SSH](https://do...

### Legacy SSH wrapper
**Path:** `/terminal/warpify/ssh-legacy`
**Summary:** {% hint style="info" %} If you are looking to troubleshoot the tmux SSH feature, see the [SSH](https://docs.warp.dev/terminal/warpify/ssh). {% endhint %}

### Warpify subshells
**Path:** `/terminal/warpify/subshells`
**Summary:** Within the context of Warp, a "subshell" is defined as any nested interactive shell session that's spawned and running within the context of an existing, running shell. This can be a nested session...

### Windows and Tabs
**Path:** `/terminal/windows`
**Summary:** 1. [Tabs](https://docs.warp.dev/terminal/windows/tabs) allow you to organize a window into multiple terminal sessions. 2. [Vertical Tabs](https://docs.warp.dev/terminal/windows/vertical-tabs) repla...

### Configurable toolbar
**Path:** `/terminal/windows/configurable-toolbar`
**Summary:** The header toolbar holds the panel toggle buttons for the tabs panel, tools panel, agent management, Code Review, and notifications mailbox. Instead of a fixed layout, you can rearrange these butto...

### Global hotkey
**Path:** `/terminal/windows/global-hotkey`
**Summary:** {% hint style="info" %} On macOS, [system keyboard shortcuts](https://support.apple.com/en-us/HT201236) like `CMD-ESC`, `CMD-BACKTICK`, `CMD-TAB`, `CMD-PERIOD`, and `CMD-TILDE` need to be [unbound]...

### Launch Configurations (Legacy)
**Path:** `/terminal/windows/launch-configurations`
**Summary:** {% hint style="warning" %} Launch Configurations have been replaced by [Tab Configs](https://docs.warp.dev/terminal/windows/tab-configs). Existing Launch Configurations continue to work, but new fe...

### Split panes
**Path:** `/terminal/windows/split-panes`
**Summary:** {% tabs %} {% tab title="macOS" %}

### Tab Configs
**Path:** `/terminal/windows/tab-configs`
**Summary:** Tab Configs let you define reusable tab setups — including directory, startup commands, pane layout, shell, and theme — in a simple TOML file. Select a Tab Config from the `+` menu to open a fully ...

### Tabs
**Path:** `/terminal/windows/tabs`
**Summary:** {% hint style="info" %} New Tabs will default to the active Tabs’ current [Working Directory](https://docs.warp.dev/terminal/more-features/working-directory) and the actual color values will be aut...

### Vertical Tabs
**Path:** `/terminal/windows/vertical-tabs`
**Summary:** The vertical tabs panel is a sidebar that replaces the traditional horizontal tab bar with a richer, more powerful tab management surface. Instead of a single row of tab titles, the panel displays ...


════════════════════════════════════════════════════════════════════════════════
## Search Patterns

Use these grep patterns to find content in `full-docs.txt`:

```bash
# Find a specific page
grep -A 100 "^PAGE: /path" full-docs.txt

# Find all pages in a section
grep -B 1 "^SECTION: SECTIONNAME" full-docs.txt | grep "^PAGE:"

# Extract a complete page (between separators)
sed -n "/^PAGE: \/your-page$/,/^\xe2\x95\x90\{80\}$/p" full-docs.txt

# Search for a keyword across all docs
grep -n "keyword" full-docs.txt
```
