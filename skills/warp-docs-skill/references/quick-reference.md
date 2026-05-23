# Warp Terminal Quick Reference

Source: https://docs.warp.dev
Generated: 2026-05-21

## Quick Navigation

| Section | Pages | Description |
|---------|-------|-------------|
| agent-platform | 91 |  |
| api | 1 |  |
| changelog | 7 |  |
| code | 9 | Code editing, review, and codebase context features |
| enterprise | 17 |  |
| getting-started | 13 | Installation, setup, keyboard shortcuts, and shell configuration |
| guides | 55 |  |
| home | 1 |  |
| knowledge-and-collaboration | 11 | Warp Drive, notebooks, workflows, teams, and sharing |
| quickstart | 1 |  |
| reference | 33 |  |
| support-and-community | 23 |  |
| terminal | 71 | Terminal features: blocks, input, output, tabs, themes, and more |

### Keyboard Shortcuts
*Source: /getting-started/keyboard-shortcuts*

> For the complete documentation index, see [llms.txt](/llms.txt).
> Markdown versions of each page are available by appending .md to any URL.

# Keyboard Shortcuts

View, customize, and remap keyboard shortcuts for all Warp features.

Warp opens with a shortcut screen showing some of the most commonly used keyboard shortcuts. Hide the shortcut screen by clicking the x button. Quickly view keyboard shortcuts via the [Command Palette](/terminal/command-palette/) or the Resource Center keyboard shortcut sidebar.

## Custom keyboard shortcuts

Set custom, clear, or default keyboard shortcuts by navigating to **Settings** > **Keyboard shortcuts**. Search through the re-mappable actions or existing shortcuts using the search bar.

Remap the keyboard shortcuts using a file. See our [keysets repository](https://github.com/warpdotdev/keysets/tree/main) for instructions.

Note

On macOS, [system keyboard shortcuts](https://support.apple.com/en-us/HT201236) like `CMD-ESC`, `CMD-BACKTICK`, `CMD-TAB`, `CMD-PERIOD`, and `CMD-TILDE` need to be [unbound](https://support.apple.com/guide/mac-help/keyboard-shortcuts-mchlp2262/mac) before you can use them in Warp.

Caution

Keybinds that conflict with others are highlighted with an orange border.

![keybinds that conflict with others are highlighted in orange](/_astro/keybinds-conflict.O8JIUjCq_Z19PQKz.webp?dpl=dpl_3o49YW1rtGc6EwUDDU5RMEZfqYnp)

An example of a keybinding conflict warning.

## All available shortcuts

-   [macOS](#tab-panel-661)
-   [Windows](#tab-panel-662)
-   [Linux](#tab-panel-663)

**Warp Essentials**

| Shortcut | Command | Action |
| --- | --- | --- |
| `CMD-D` | Split Pane Right | `pane_group:add_right` |
| `CTRL-CMD-L` | Launch Configuration Palette | `workspace:toggle_launch_config_palette` |
| `CTRL-CMD-T` | Open Theme Picker | `workspace:show_theme_chooser` |
| `CTRL-R` | Command Search | `workspace:show_command_search` |
| `CTRL-SHIFT-R` | Workflows | `input:toggle_workflows` |
| `` CTRL-` `` | Generate | `input:toggle_natural_language_command_search` |
| `CMD-L` | Focus Terminal Input | `terminal:focus_input` |
| `CTRL-I` | Warpify Subshell | `terminal:trigger_subshell_bootstrap` |
| `CMD-\` | Warp Drive | `terminal:toggle_warp_drive` |
| `CMD-O` | File search |  |
| `CMD-P` | Open Command Palette |  |

**Blocks**

*[See full documentation for more...]*

────────────────────────────────────────────────────────────────────────────────

### Supported Shells
*Source: /getting-started/supported-shells*

> For the complete documentation index, see [llms.txt](/llms.txt).
> Markdown versions of each page are available by appending .md to any URL.

# Supported Shells

Warp supports bash, zsh, fish, PowerShell, and WSL2 across macOS, Windows, and Linux.

Warp supports bash, zsh, fish, and PowerShell (pwsh) across macOS, Windows, and Linux, loading your login shell by default. You can change the default shell per-session, customize each shell’s configuration files and environment variables, and install additional shells like fish or PowerShell on macOS.

## Warp default shell

Warp tries to load your login shell by default. Currently, Warp supports bash, fish, zsh, and PowerShell (pwsh). If your login shell is set to something else (e.g. Nushell) Warp will show a banner indicating it’s not supported and load the default shells listed below:

-   On macOS, zsh is the default shell.
-   On Windows, PowerShell (pwsh) is the default shell.
-   On Linux, bash is the default shell.

Note

If you run into issues configuring your RC files (`~/.bashrc`, `~/.zshrc`, `config.fish`, `Microsoft.PowerShell_profile.ps1`) with Warp, please see [Configuring and debugging your RC files](/support-and-community/troubleshooting-and-support/known-issues/#configuring-and-debugging-your-rc-files).

### Changing what shell Warp uses

To change the default shell, we recommend you choose a shell in Warp by going to **Settings** > **Features** and scrolling to the `Session` section, then select the “Startup shell for new sessions”

Note

The changes to your shell will only take effect when you start a new session.

## Customizing your shell environment

### Customize your zsh shell environment

Zsh can be customized via the `~/.zshrc` file, which runs whenever a new session starts (window, tab, or pane). Use it to set environment variables, aliases, and customize the [prompt](/terminal/appearance/prompt/).

#### Editing the .zshrc file

Edit `~/.zshrc` using `nano ~/.zshrc` or `vi ~/.zshrc`.

Note

Files starting with a dot (`.`) are hidden by default. Check your file explorer’s settings to show hidden files.

#### Reloading the zshrc file

Apply changes by running `source ~/.zshrc` or restarting Warp/opening a new session.

### Customize your Bash shell environment

*[See full documentation for more...]*

────────────────────────────────────────────────────────────────────────────────

### Migrate to Warp
*Source: /getting-started/migrate-to-warp*

> For the complete documentation index, see [llms.txt](/llms.txt).
> Markdown versions of each page are available by appending .md to any URL.

# Migrate to Warp

Move your settings and mental model into Warp. Pick the tool you're coming from for step-by-step guidance and Warp equivalents.

Warp users come from every kind of terminal, editor, and AI coding tool. This section has a dedicated page for each of the most common sources, with step-by-step migration guidance, notes on what transfers automatically, and a cross-reference for the Warp features that replace what you use today.

Pick the tool you’re switching from:

-   [**Claude Code**](/getting-started/migrate-to-warp/migrate-to-warp-from-claude-code/) - use Claude Code inside Warp, or switch from Claude Code to Warp’s built-in Agent Mode. Covers context, rules, and model setup.
-   [**Cursor**](/getting-started/migrate-to-warp/migrate-to-warp-from-cursor/) - use Warp alongside Cursor as your agent terminal, or replace Cursor entirely with Warp’s built-in code editor and Agent Mode.
-   [**Ghostty**](/getting-started/migrate-to-warp/migrate-to-warp-from-ghostty/) - translate your Ghostty config to Warp and find equivalents for quick terminal, tabs, and GPU rendering.
-   [**iTerm2**](/getting-started/migrate-to-warp/migrate-to-warp-from-iterm2/) - use Warp’s built-in iTerm2 importer to transfer themes, fonts, keybindings, and hotkey windows in a few clicks.
-   [**macOS Terminal**](/getting-started/migrate-to-warp/migrate-to-warp-from-macos-terminal/) - match your Terminal.app setup and discover the split panes, tabs, and Agent Mode features Terminal.app lacks.
-   [**VS Code terminal**](/getting-started/migrate-to-warp/migrate-to-warp-from-vs-code-terminal/) - use Warp alongside VS Code for a richer terminal, or replace VS Code entirely with Warp’s built-in code editor.
-   [**Windows Terminal**](/getting-started/migrate-to-warp/migrate-to-warp-from-windows-terminal/) - map Windows Terminal profiles, PowerShell settings, and color schemes into Warp on Windows.

## Coming from something else?

Warp works well for developers migrating from many other sources. If you’re switching from a tool that isn’t listed above - for example, Alacritty, WezTerm, Kitty, Hyper, or a Linux default like GNOME Terminal or Konsole - drop a note in our [Discord community](https://discord.gg/warpdotdev) so we can prioritize coverage.

────────────────────────────────────────────────────────────────────────────────

### Terminal Blocks overview
*Source: /terminal/blocks*

> For the complete documentation index, see [llms.txt](/llms.txt).
> Markdown versions of each page are available by appending .md to any URL.

# Terminal Blocks overview

A Block groups commands and outputs into one atomic unit.

Blocks are Warp’s fundamental unit for organizing terminal output. Every command and its output is grouped into a single Block that you can copy, search, filter, bookmark, share, and navigate independently — replacing the endless scroll of traditional terminals with structured, actionable output.

## What are Blocks?

Blocks enable us to easily:

-   Copy a command
-   Copy a command’s output
-   Scroll directly to the start of a command’s output
-   Re-input commands
-   Share both a command and its output (with formatting!)
-   Bookmark commands

Note

Interested in how we differentiate input and output, or how we implement blocks? Check out our blog post: [How Warp Works.](https://www.warp.dev/blog/how-warp-works/#implementing-blocks)

![Intro to Blocks](https://i.ytimg.com/vi/PH1u0TZ5Lf0/sddefault.jpg)

![Blocks](/_astro/annotated_blocks-1.CLvjDB1C_bRTPh.webp?dpl=dpl_3o49YW1rtGc6EwUDDU5RMEZfqYnp)

────────────────────────────────────────────────────────────────────────────────

### Modern text editing overview
*Source: /terminal/editor*

> For the complete documentation index, see [llms.txt](/llms.txt).
> Markdown versions of each page are available by appending .md to any URL.

# Modern text editing overview

Unlike other terminals, Warp’s input editor operates out of the box like a modern IDE and the text editors we’re used to.

Warp’s input editor works like a modern IDE text editor, with cursor movement, click-to-place, multi-line editing, copy-paste, word selection, and soft wrapping built in. Unlike traditional terminals, you can edit commands the same way you edit code — no memorizing shell-specific shortcuts required.

Note

Text Editor Input also works for [SSH sessions](/terminal/warpify/ssh/).

### Soft Wrapping

Warp supports soft wrapping in the input editor. If an autosuggestion goes off-screen, the input editor will be horizontally scrollable to make it visible. Some operations treat soft-wrapped lines like a logical line (`TRIPLE-CLICK`) while other operations treat soft wrapped lines like visible different lines (`UP`/`DOWN`, `SHIFT-UP`/`SHIFT-DOWN`).

### Copy on Select

Warp supports copy on select for selectable text within [Blocks](/terminal/blocks/).

-   Toggle this feature **Settings** > **Features** > **Terminal** or search for “Copy on select” in the [Command Palette](/terminal/command-palette/).

### Autocomplete quotes, parentheses, and brackets

Warp can automatically complete quotes, brackets, and parentheses like you’re used to in IDEs.

-   Toggle this feature **Settings** > **Features** > **Text Editing** or search for “Autocomplete quotes” in the [Command Palette](/terminal/command-palette/).

## How to use it

-   [macOS](#tab-panel-758)
-   [Windows](#tab-panel-759)
-   [Linux](#tab-panel-760)

*[See full documentation for more...]*

────────────────────────────────────────────────────────────────────────────────

### Command entry overview
*Source: /terminal/entry*

> For the complete documentation index, see [llms.txt](/llms.txt).
> Markdown versions of each page are available by appending .md to any URL.

# Command entry overview

Warp's main features for Command Entry, History, Synchronized Inputs, YAML Workflows and More!

1.  [Command Corrections](/terminal/entry/command-corrections/) provides auto-correct suggestions on previously run commands to catch typos, and forgotten flags, and fix general console errors.
2.  [Command Search](/terminal/entry/command-search/) is a 3-in-1 panel that allows you to search across Command History, Workflows, Notebooks, and AI Command Search all at once.
3.  [Command History](/terminal/entry/command-history/) allows Warp to isolate the history of each shell session to make previously run commands easily accessible.
4.  [Synchronized Inputs](/terminal/entry/synchronized-inputs/) allow you to easily run the same command in multiple sessions at the same time.
5.  [YAML Workflows](/terminal/entry/yaml-workflows/) are easier to execute and share parameterized and searchable commands within Warp.

## Command Corrections

## Command Search

## Command History

## YAML Workflows

────────────────────────────────────────────────────────────────────────────────

### Warp Drive overview
*Source: /knowledge-and-collaboration/warp-drive*

> For the complete documentation index, see [llms.txt](/llms.txt).
> Markdown versions of each page are available by appending .md to any URL.

# Warp Drive overview

Warp Drive is a workspace in your terminal where you can save Workflows, Notebooks, Prompts, and Environment Variables for personal use or to share with a team.

Warp Drive is a built-in workspace for saving and sharing Workflows, Notebooks, Prompts, and Environment Variables across your team. All objects sync in real time, so you and your team always have access to the latest versions, whether you’re working locally or collaborating across an organization.

## What is Warp Drive?

All objects stored in Warp Drive sync immediately as they’re updated, so you and your team will always have access to the latest versions.

![Warp Drive Overview](https://i.ytimg.com/vi/AGL0YcRj5-o/sddefault.jpg)

## How to access it

-   [macOS](#tab-panel-670)
-   [Windows](#tab-panel-671)
-   [Linux](#tab-panel-672)

Warp Drive is accessible from the status bar in Warp or you can toggle the Warp Drive side panel with `CMD-\`.

Warp Drive is accessible from the status bar in Warp or you can toggle the Warp Drive side panel with `CTRL-SHIFT-\`.

Warp Drive is accessible from the status bar in Warp or you can toggle the Warp Drive side panel with `CTRL-SHIFT-\`.

![Warp Drive icon on top left corner of Warp](/_astro/Open_Warp_Drive.CdkFmU8u_Z1B1uF6.webp?dpl=dpl_3o49YW1rtGc6EwUDDU5RMEZfqYnp)

The Warp Drive icon in the top-left corner.

## Workspaces in Warp Drive

When you open the Warp Drive panel, you will find a personal workspace where you can store your Workflows, Notebooks, Prompts, and Environment Variables and organize them into folders.

![Personal workspace zero state in Warp Drive, showing where Workflows, Notebooks, Prompts, and Environment Variables are saved.](/_astro/Warp_Drive_Zero_State.ChcuOCHL_U7Smd.webp?dpl=dpl_3o49YW1rtGc6EwUDDU5RMEZfqYnp)

If you are a member of a team using Warp Drive, your team’s workspace will also be available in the side panel.

![Warp Drive side panel showing both a personal workspace and a team workspace.](/_astro/Warp_Drive_with_Team.DL2nCgiJ_1R1Ujq.webp?dpl=dpl_3o49YW1rtGc6EwUDDU5RMEZfqYnp)

## Organizing objects in Warp Drive with your team

*[See full documentation for more...]*

────────────────────────────────────────────────────────────────────────────────
