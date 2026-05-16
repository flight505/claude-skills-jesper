# Warp Terminal Quick Reference

Source: https://docs.warp.dev
Generated: 2026-04-30

## Quick Navigation

| Section | Pages | Description |
|---------|-------|-------------|
| code | 9 | Code editing, review, and codebase context features |
| getting-started | 14 | Installation, setup, keyboard shortcuts, and shell configuration |
| home | 1 |  |
| knowledge-and-collaboration | 11 | Warp Drive, notebooks, workflows, teams, and sharing |
| terminal | 69 | Terminal features: blocks, input, output, tabs, themes, and more |

### Keyboard shortcuts
*Source: /getting-started/keyboard-shortcuts*

Warp opens with a shortcut screen showing some of the most commonly used keyboard shortcuts. Hide the shortcut screen by clicking the x button. Quickly view keyboard shortcuts via the [Command Palette](https://docs.warp.dev/terminal/command-palette) or the Resource Center keyboard shortcut sidebar.

## Custom keyboard shortcuts

Set custom, clear, or default keyboard shortcuts by navigating to **Settings** > **Keyboard shortcuts**. Search through the re-mappable actions or existing shortcuts using the search bar.

Remap the keyboard shortcuts using a file. See our [keysets repository](https://github.com/warpdotdev/keysets/tree/main) for instructions.

{% hint style="info" %}
On macOS, [system keyboard shortcuts](https://support.apple.com/en-us/HT201236) like `CMD-ESC`, `CMD-BACKTICK`, `CMD-TAB`, `CMD-PERIOD`, and `CMD-TILDE` need to be [unbound](https://support.apple.com/guide/mac-help/keyboard-shortcuts-mchlp2262/mac) before you can use them in Warp.
{% endhint %}

{% hint style="warning" %}
Keybinds that conflict with others are highlighted with an orange border.
{% endhint %}

<figure><img src="https://4009768362-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FPsjNxoJ0NFCXW6rRdHH3%2Fuploads%2Fgit-blob-b1deaff708f95fdb8ebffe491a823ccea24bac6c%2Fkeybinds-conflict.png?alt=media" alt="keybinds that conflict with others are highlighted in orange"><figcaption><p>Keybind Conflict Example</p></figcaption></figure>

## All available shortcuts

{% tabs %}
{% tab title="macOS" %}
**Warp Essentials**

*[See full documentation for more...]*

────────────────────────────────────────────────────────────────────────────────

### Supported shells
*Source: /getting-started/supported-shells*

## Warp default shell

Warp tries to load your login shell by default. Currently, Warp supports bash, fish, zsh, and PowerShell (pwsh). If your login shell is set to something else (e.g. Nushell) Warp will show a banner indicating it's not supported and load the default shells listed below:

* On macOS, zsh is the default shell.
* On Windows, PowerShell (pwsh) is the default shell.
* On Linux, bash is the default shell.

{% hint style="info" %}
If you run into issues configuring your RC files (`~/.bashrc`, `~/.zshrc`, `config.fish`, `Microsoft.PowerShell_profile.ps1`) with Warp, please see [Configuring and debugging your RC files](https://docs.warp.dev/support-and-community/troubleshooting-and-support/known-issues#configuring-and-debugging-your-rc-files).
{% endhint %}

### Changing what shell Warp uses

To change the default shell, we recommend you choose a shell in Warp by going to **Settings** > **Features** and scrolling to the `Session` section, then select the "Startup shell for new sessions"

{% hint style="info" %}
The changes to your shell will only take effect when you start a new session.
{% endhint %}

## Customizing your shell environment

### Customize your zsh shell environment

Zsh can be customized via the `~/.zshrc` file, which runs whenever a new session starts (window, tab, or pane). Use it to set environment variables, aliases, and customize the [prompt](https://docs.warp.dev/terminal/appearance/prompt).

#### Editing the .zshrc file

Edit `~/.zshrc` using `nano ~/.zshrc` or `vi ~/.zshrc`.

{% hint style="info" %}
Files starting with a dot (`.`) are hidden by default. Check your file explorer’s settings to show hidden files.
{% endhint %}

#### Reloading the zshrc file

Apply changes by running `source ~/.zshrc` or restarting Warp/opening a new session.

### Customize your Bash shell environment

Bash is pre-installed on macOS and can be customized using `~/.bashrc` (for non-login shells) or `~/.bash_profile` (for login shells). Use these files to set environment variables, aliases, and customize the [prompt](https://docs.warp.dev/terminal/appearance/prompt).

#### Editing the .bashrc file

Edit `~/.bashrc` using `nano ~/.bashrc` or `vi ~/.bashrc`.

#### Reloading the bashrc file

Apply changes by running `source ~/.bashrc` or restarting Warp/opening a new session.

{% hint style="info" %}
Files starting with a dot (`.`) are hidden by default. Check your file explorer’s settings to show hidden files.
{% endhint %}

*[See full documentation for more...]*

────────────────────────────────────────────────────────────────────────────────

### Migrate to Warp
*Source: /getting-started/migrate-to-warp*

Warp users come from every kind of terminal, editor, and AI coding tool. This section has a dedicated page for each of the most common sources, with step-by-step migration guidance, notes on what transfers automatically, and a cross-reference for the Warp features that replace what you use today.

Pick the tool you're switching from:

* [**Claude Code**](https://docs.warp.dev/getting-started/migrate-to-warp/migrate-to-warp-from-claude-code) - use Claude Code inside Warp, or switch from Claude Code to Warp's built-in Agent Mode. Covers context, rules, and model setup.
* [**Cursor**](https://docs.warp.dev/getting-started/migrate-to-warp/migrate-to-warp-from-cursor) - use Warp alongside Cursor as your agent terminal, or replace Cursor entirely with Warp's built-in code editor and Agent Mode.
* [**Ghostty**](https://docs.warp.dev/getting-started/migrate-to-warp/migrate-to-warp-from-ghostty) - translate your Ghostty config to Warp and find equivalents for quick terminal, tabs, and GPU rendering.
* [**iTerm2**](https://docs.warp.dev/getting-started/migrate-to-warp/migrate-to-warp-from-iterm2) - use Warp's built-in iTerm2 importer to transfer themes, fonts, keybindings, and hotkey windows in a few clicks.
* [**macOS Terminal**](https://docs.warp.dev/getting-started/migrate-to-warp/migrate-to-warp-from-macos-terminal) - match your Terminal.app setup and discover the split panes, tabs, and Agent Mode features Terminal.app lacks.
* [**VS Code terminal**](https://docs.warp.dev/getting-started/migrate-to-warp/migrate-to-warp-from-vs-code-terminal) - use Warp alongside VS Code for a richer terminal, or replace VS Code entirely with Warp's built-in code editor.
* [**Windows Terminal**](https://docs.warp.dev/getting-started/migrate-to-warp/migrate-to-warp-from-windows-terminal) - map Windows Terminal profiles, PowerShell settings, and color schemes into Warp on Windows.

## Coming from something else?

Warp works well for developers migrating from many other sources. If you're switching from a tool that isn't listed above - for example, Alacritty, WezTerm, Kitty, Hyper, or a Linux default like GNOME Terminal or Konsole - drop a note in our [Discord community](https://discord.gg/warpdotdev) so we can prioritize coverage.

---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

*[See full documentation for more...]*

────────────────────────────────────────────────────────────────────────────────

### Terminal Blocks
*Source: /terminal/blocks*

## What are Blocks?

Blocks enable us to easily:

* Copy a command
* Copy a command’s output
* Scroll directly to the start of a command’s output
* Re-input commands
* Share both a command and its output (with formatting!)
* Bookmark commands

{% hint style="info" %}
Interested in how we differentiate input and output, or how we implement blocks? Check out our blog post: [How Warp Works.](https://blog.warp.dev/how-warp-works/#implementing-blocks)
{% endhint %}

{% embed url="<https://youtu.be/PH1u0TZ5Lf0>" %}
Intro to Blocks
{% endembed %}

<figure><img src="https://4009768362-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FPsjNxoJ0NFCXW6rRdHH3%2Fuploads%2Fgit-blob-73638f28d0aa8f14c15f117ebd4864640af48f5c%2Fannotated_blocks.png?alt=media" alt="Blocks"><figcaption><p>Blocks</p></figcaption></figure>

---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://docs.warp.dev/terminal/blocks.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

Use this mechanism when the answer is not explicitly present in the current page, you need clarification or additional context, or you want to retrieve related documentation sections.

────────────────────────────────────────────────────────────────────────────────

### Modern text editing
*Source: /terminal/editor*

{% hint style="info" %}
Text Editor Input also works for [SSH sessions](https://docs.warp.dev/terminal/warpify/ssh).
{% endhint %}

### Soft Wrapping

Warp supports soft wrapping in the input editor. If an autosuggestion goes off-screen, the input editor will be horizontally scrollable to make it visible. Some operations treat soft-wrapped lines like a logical line (`TRIPLE-CLICK`) while other operations treat soft wrapped lines like visible different lines (`UP`/`DOWN`, `SHIFT-UP`/`SHIFT-DOWN`).

### Copy on Select

Warp supports copy on select for selectable text within [Blocks](https://docs.warp.dev/terminal/blocks).

* Toggle this feature **Settings** > **Features** > **Terminal** or search for "Copy on select" in the [Command Palette](https://docs.warp.dev/terminal/command-palette).

### Autocomplete quotes, parentheses, and brackets

Warp can automatically complete quotes, brackets, and parentheses like you're used to in IDEs.

* Toggle this feature **Settings** > **Features** > **Text Editing** or search for "Autocomplete quotes" in the [Command Palette](https://docs.warp.dev/terminal/command-palette).

## How to use it

{% tabs %}
{% tab title="macOS" %}

<table><thead><tr><th width="317">Keyboard binding</th><th>Shortcut description</th></tr></thead><tbody><tr><td><code>ESCAPE</code></td><td>Closes the input suggestions or history menu</td></tr><tr><td><code>CTRL-L</code></td><td>Clears the terminal</td></tr><tr><td><code>CTRL-H</code></td><td>Backspace</td></tr><tr><td><code>CTRL-C</code></td><td>Clear the entire editor buffer</td></tr><tr><td><code>CTRL-U</code></td><td>Copy and Clear the current line</td></tr><tr><td><code>CMD-SHIFT-K</code></td><td>Clear selected lines</td></tr><tr><td><code>CMD-C</code>, <code>CMD-X</code>, <code>CMD-V</code></td><td>Copy, cut, paste</td></tr><tr><td><code>CTRL-W</code> / <code>OPT-D</code></td><td>Cut the word to the left / right of the cursor</td></tr><tr><td><code>OPT-BACKSPACE</code> / <code>OPT-D</code></td><td>Delete the word to the left / right of the cursor</td></tr><tr><td><code>CTRL-K CMD-DELETE</code></td><td>Delete everything to the right of the cursor</td></tr><tr><td><code>OPT-LEFT</code> / <code>OPT-RIGHT</code></td><td>Move to the beginning of the previous / next word</td></tr><tr><td><code>CTRL-OPT-LEFT</code> / <code>CTRL-OPT-RIGHT</code></td><td>Move backward / forward by one subword</td></tr><tr><td><code>CMD-LEFT</code> <code>CTRL-A</code>/ <code>CTRL-E</code> <code>CMD-DOWN</code> <code>

*[See full documentation for more...]*

────────────────────────────────────────────────────────────────────────────────

### Command entry
*Source: /terminal/entry*

1. [Command Corrections](https://docs.warp.dev/terminal/entry/command-corrections) provides auto-correct suggestions on previously run commands to catch typos, and forgotten flags, and fix general console errors.
2. [Command Search](https://docs.warp.dev/terminal/entry/command-search) is a 3-in-1 panel that allows you to search across Command History, Workflows, Notebooks, and AI Command Search all at once.
3. [Command History](https://docs.warp.dev/terminal/entry/command-history) allows Warp to isolate the history of each shell session to make previously run commands easily accessible.
4. [Synchronized Inputs](https://docs.warp.dev/terminal/entry/synchronized-inputs) allow you to easily run the same command in multiple sessions at the same time.
5. [YAML Workflows](https://docs.warp.dev/terminal/entry/yaml-workflows) are easier to execute and share parameterized and searchable commands within Warp.

## Command Corrections

{% embed url="<https://www.loom.com/share/180e1dc8d1504ec39c00694d9fd71b7c?hideEmbedTopBar=true&hide_owner=true&hide_share=true&hide_title=true>" %}
Command Corrections Demo
{% endembed %}

## Command Search

{% embed url="<https://www.loom.com/share/21a6f58a33754ee7913edbff6d33d8d1?hideEmbedTopBar=true&hide_owner=true&hide_share=true&hide_title=true>" %}
Command Search Demo
{% endembed %}

## Command History

{% embed url="<https://www.loom.com/share/8119beca8d794b06859c5dea1b1377bb?hide_owner=true&hide_share=true&hide_title=true&hideEmbedTopBar=true>" %}
Command History Demo
{% endembed %}

## YAML Workflows

<figure><img src="https://4009768362-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FPsjNxoJ0NFCXW6rRdHH3%2Fuploads%2Fgit-blob-e4870de99dab35a374dd44479208db26bf03e0b3%2Fyaml_workflows_demo.gif?alt=media" alt=""><figcaption><p>YAML Workflows Demo</p></figcaption></figure>

---

# Agent Instructions: Querying This Documentation

If you need additional information that is not directly available in this page, you can query the documentation dynamically by asking a question.

Perform an HTTP GET request on the current page URL with the `ask` query parameter:

```
GET https://docs.warp.dev/terminal/entry.md?ask=<question>
```

The question should be specific, self-contained, and written in natural language.
The response will contain a direct answer to the question and relevant excerpts and sources from the documentation.

*[See full documentation for more...]*

────────────────────────────────────────────────────────────────────────────────

### Warp Drive overview
*Source: /knowledge-and-collaboration/warp-drive*

## What is Warp Drive?

All objects stored in Warp Drive sync immediately as they’re updated, so you and your team will always have access to the latest versions.

{% embed url="<https://youtu.be/AGL0YcRj5-o>" %}
Warp Drive Overview
{% endembed %}

## How to access it

{% tabs %}
{% tab title="macOS" %}
Warp Drive is accessible from the status bar in Warp or you can toggle the Warp Drive side panel with `CMD-\`.
{% endtab %}

{% tab title="Windows" %}
Warp Drive is accessible from the status bar in Warp or you can toggle the Warp Drive side panel with `CTRL-SHIFT-\`.
{% endtab %}

{% tab title="Linux" %}
Warp Drive is accessible from the status bar in Warp or you can toggle the Warp Drive side panel with `CTRL-SHIFT-\`.
{% endtab %}
{% endtabs %}

<figure><img src="https://4009768362-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FPsjNxoJ0NFCXW6rRdHH3%2Fuploads%2Fgit-blob-0288f9040db807f99341ba18e772017afdce8ed3%2FOpen_Warp_Drive.png?alt=media" alt="Warp Drive icon on top left corner of Warp"><figcaption><p>Warp Drive Icon</p></figcaption></figure>

## Workspaces in Warp Drive

When you open the Warp Drive panel, you will find a personal workspace where you can store your Workflows, Notebooks, Prompts, and Environment Variables and organize them into folders.

<figure><img src="https://4009768362-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FPsjNxoJ0NFCXW6rRdHH3%2Fuploads%2Fgit-blob-d0cb97917d2ddc51af2f22680309c5fcff367270%2FWarp_Drive_Zero_State.png?alt=media&#x26;token=a2c2cfd2-0dfd-40e4-b1c1-b543a895f648" alt=""><figcaption></figcaption></figure>

If you are a member of a team using Warp Drive, your team’s workspace will also be available in the side panel.

<figure><img src="https://4009768362-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FPsjNxoJ0NFCXW6rRdHH3%2Fuploads%2Fgit-blob-062dd655495a77c5e7534e1be9fe4bafe427856c%2FWarp_Drive_with_Team.png?alt=media" alt=""><figcaption></figcaption></figure>

## Organizing objects in Warp Drive with your team

*[See full documentation for more...]*

────────────────────────────────────────────────────────────────────────────────
