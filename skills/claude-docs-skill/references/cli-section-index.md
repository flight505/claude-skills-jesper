# Claude Code CLI Documentation Index

Organized reference for finding topics.
Use grep on `cli-full-docs.txt` for full content.

## All Pages

### Advanced setup
**Path:** `/setup.md`
**Summary:** System requirements, platform-specific installation, version management, and uninstallation for Claude Code.

### Agent SDK overview
**Path:** `/agent-sdk/overview.md`
**Summary:** Build production AI agents with Claude Code as a library

### Agent SDK reference - Python
**Path:** `/agent-sdk/python.md`
**Summary:** Complete API reference for the Python Agent SDK, including all functions, types, and classes.

### Agent SDK reference - TypeScript
**Path:** `/agent-sdk/typescript.md`
**Summary:** Complete API reference for the TypeScript Agent SDK, including all functions, types, and interfaces.

### Agent Skills in the SDK
**Path:** `/agent-sdk/skills.md`
**Summary:** Extend Claude with specialized capabilities using Agent Skills in the Claude Agent SDK

### Authentication
**Path:** `/authentication.md`
**Summary:** Log in to Claude Code and configure authentication for individuals, teams, and organizations.

### Automate work with routines
**Path:** `/routines.md`
**Summary:** Put Claude Code on autopilot. Define routines that run on a schedule, trigger on API calls, or react to GitHub events from Anthropic-managed cloud infrastructure.

### Automate workflows with hooks
**Path:** `/hooks-guide.md`
**Summary:** Run shell commands automatically when Claude Code edits files, finishes tasks, or needs input. Format code, send notifications, validate commands, and enforce project rules.

### Best practices for Claude Code
**Path:** `/best-practices.md`
**Summary:** Tips and patterns for getting the most out of Claude Code, from configuring your environment to scaling across parallel sessions.

### Champion kit
**Path:** `/champion-kit.md`
**Summary:** A playbook for engineers advocating Claude Code internally: what to share, how to answer questions, and how to grow adoption on your team.

### Changelog
**Path:** `/changelog.md`
**Summary:** Release notes for Claude Code, including new features, improvements, and bug fixes by version.

### Channels reference
**Path:** `/channels-reference.md`
**Summary:** Build an MCP server that pushes webhooks, alerts, and chat messages into a Claude Code session. Reference for the channel contract: capability declaration, notification events, reply tools, sender gating, and permission relay.

### Checkpointing
**Path:** `/checkpointing.md`
**Summary:** Track, rewind, and summarize Claude's edits and conversation to manage session state.

### Choose a permission mode
**Path:** `/permission-modes.md`
**Summary:** Control whether Claude asks before editing files or running commands. Cycle modes with Shift+Tab in the CLI or use the mode selector in VS Code, Desktop, and claude.ai.

### Claude Code GitHub Actions
**Path:** `/github-actions.md`
**Summary:** Learn about integrating Claude Code into your development workflow with Claude Code GitHub Actions

### Claude Code GitLab CI/CD
**Path:** `/gitlab-ci-cd.md`
**Summary:** Learn about integrating Claude Code into your development workflow with GitLab CI/CD

### Claude Code in Slack
**Path:** `/slack.md`
**Summary:** Delegate coding tasks directly from your Slack workspace

### Claude Code on Amazon Bedrock
**Path:** `/amazon-bedrock.md`
**Summary:** Learn about configuring Claude Code through Amazon Bedrock, including setup, IAM configuration, and troubleshooting.

### Claude Code on Claude Platform on AWS
**Path:** `/claude-platform-on-aws.md`
**Summary:** Configure Claude Code to use the Anthropic-operated Claude API with AWS authentication, IAM access control, and AWS Marketplace billing.

### Claude Code on Google Vertex AI
**Path:** `/google-vertex-ai.md`
**Summary:** Learn about configuring Claude Code through Google Vertex AI, including setup, IAM configuration, and troubleshooting.

### Claude Code on Microsoft Foundry
**Path:** `/microsoft-foundry.md`
**Summary:** Learn about configuring Claude Code through Microsoft Foundry, including setup, configuration, and troubleshooting.

### Claude Code settings
**Path:** `/settings.md`
**Summary:** Configure Claude Code with global and project-level settings, and environment variables.

### Claude Code with GitHub Enterprise Server
**Path:** `/github-enterprise-server.md`
**Summary:** Connect Claude Code to your self-hosted GitHub Enterprise Server instance for web sessions, code review, and plugin marketplaces.

### CLI reference
**Path:** `/cli-reference.md`
**Summary:** Complete reference for Claude Code command-line interface, including commands and flags.

### Code Review
**Path:** `/code-review.md`
**Summary:** Set up automated PR reviews that catch logic errors, security vulnerabilities, and regressions using multi-agent analysis of your full codebase

### Commands
**Path:** `/commands.md`
**Summary:** Complete reference for commands available in Claude Code, including built-in commands and bundled skills.

### Common workflows
**Path:** `/common-workflows.md`
**Summary:** Step-by-step guides for exploring codebases, fixing bugs, refactoring, testing, and other everyday tasks with Claude Code.

### Communications kit
**Path:** `/communications-kit.md`
**Summary:** Launch announcements, drip-campaign messages, and FAQ responses for rolling Claude Code out to your engineering organization.

### Configure auto mode
**Path:** `/auto-mode-config.md`
**Summary:** Tell the auto mode classifier which repos, buckets, and domains your organization trusts. Set environment context, override the default block and allow rules, and inspect your effective config with the auto-mode CLI subcommands.

### Configure permissions
**Path:** `/agent-sdk/permissions.md`
**Summary:** Control how your agent uses tools with permission modes, hooks, and declarative allow/deny rules.

### Configure permissions
**Path:** `/permissions.md`
**Summary:** Control what Claude Code can access and do with fine-grained permission rules, modes, and managed policies.

### Configure server-managed settings
**Path:** `/server-managed-settings.md`
**Summary:** Centrally configure Claude Code for your organization through server-delivered settings, without requiring device management infrastructure.

### Configure your terminal for Claude Code
**Path:** `/terminal-config.md`
**Summary:** Fix Shift+Enter for newlines, get a terminal bell when Claude finishes, configure tmux, match the color theme, and enable Vim mode in the Claude Code CLI.

### Connect Claude Code to tools via MCP
**Path:** `/mcp.md`
**Summary:** Learn how to connect Claude Code to your tools with the Model Context Protocol.

### Connect to external tools with MCP
**Path:** `/agent-sdk/mcp.md`
**Summary:** Configure MCP servers to extend your agent with external tools. Covers transport types, tool search for large tool sets, authentication, and error handling.

### Constrain plugin dependency versions
**Path:** `/plugin-dependencies.md`
**Summary:** Declare version constraints on plugin dependencies so your plugin keeps working when an upstream plugin ships a breaking change.

### Continue local sessions from any device with Remote Control
**Path:** `/remote-control.md`
**Summary:** Continue a local Claude Code session from your phone, tablet, or any browser using Remote Control. Works with claude.ai/code and the Claude mobile app.

### Create and distribute a plugin marketplace
**Path:** `/plugin-marketplaces.md`
**Summary:** Build and host plugin marketplaces to distribute Claude Code extensions across teams and communities.

### Create custom subagents
**Path:** `/sub-agents.md`
**Summary:** Create and use specialized AI subagents in Claude Code for task-specific workflows and improved context management.

### Create plugins
**Path:** `/plugins.md`
**Summary:** Create custom plugins to extend Claude Code with skills, agents, hooks, and MCP servers.

### Customize keyboard shortcuts
**Path:** `/keybindings.md`
**Summary:** Customize keyboard shortcuts in Claude Code with a keybindings configuration file.

### Customize your status line
**Path:** `/statusline.md`
**Summary:** Configure a custom status bar to monitor context window usage, costs, and git status in Claude Code

### Data usage
**Path:** `/data-usage.md`
**Summary:** Learn about Anthropic's data usage policies for Claude

### Debug your configuration
**Path:** `/debug-your-config.md`
**Summary:** Diagnose why CLAUDE.md, settings, hooks, MCP servers, or skills aren't taking effect. Use /context, /doctor, /hooks, and /mcp to see what actually loaded.

### Desktop application
**Path:** `/desktop.md`
**Summary:** Get more out of Claude Code Desktop: parallel sessions with Git isolation, drag-and-drop pane layout, integrated terminal and file editor, side chats, computer use, Dispatch sessions from your phone, visual diff review, app previews, PR monitoring, connectors, and enterprise configuration.

### Desktop changelog
**Path:** `/desktop-changelog.md`
**Summary:** Release notes for Claude Code on Desktop, covering new features, improvements, and bug fixes by Desktop app version.

### Development containers
**Path:** `/devcontainer.md`
**Summary:** Run Claude Code inside a dev container for consistent, isolated environments across your team.

### Discover and install prebuilt plugins through marketplaces
**Path:** `/discover-plugins.md`
**Summary:** Find and install plugins from marketplaces to extend Claude Code with new skills, agents, and capabilities.

### Enterprise deployment overview
**Path:** `/third-party-integrations.md`
**Summary:** Learn how Claude Code can integrate with various third-party services and infrastructure to meet enterprise deployment requirements.

### Enterprise network configuration
**Path:** `/network-config.md`
**Summary:** Configure Claude Code for enterprise environments with proxy servers, custom Certificate Authorities (CA), and mutual Transport Layer Security (mTLS) authentication.

### Environment variables
**Path:** `/env-vars.md`
**Summary:** Reference for environment variables that control Claude Code behavior.

### Error reference
**Path:** `/errors.md`
**Summary:** Look up Claude Code runtime error messages with what each one means and how to fix it.

### Explore the .claude directory
**Path:** `/claude-directory.md`
**Summary:** Where Claude Code reads CLAUDE.md, settings.json, hooks, skills, commands, subagents, rules, and auto memory. Explore the .claude directory in your project and ~/.claude in your home directory.

### Explore the context window
**Path:** `/context-window.md`
**Summary:** An interactive simulation of how Claude Code's context window fills during a session. See what loads automatically, what each file read costs, and when rules and hooks fire.

### Extend Claude Code
**Path:** `/features-overview.md`
**Summary:** Understand when to use CLAUDE.md, Skills, subagents, hooks, MCP, and plugins.

### Extend Claude with skills
**Path:** `/skills.md`
**Summary:** Create, manage, and share skills to extend Claude's capabilities in Claude Code. Includes custom commands and bundled skills.

### Find bugs with ultrareview
**Path:** `/ultrareview.md`
**Summary:** Run a deep, multi-agent code review in the cloud with /ultrareview to find and verify bugs before you merge.

### Fullscreen rendering
**Path:** `/fullscreen.md`
**Summary:** Enable a smoother, flicker-free rendering mode with mouse support and stable memory usage in long conversations.

### Get started with Claude Code on the web
**Path:** `/web-quickstart.md`
**Summary:** Run Claude Code in the cloud from your browser or phone. Connect a GitHub repository, submit a task, and review the PR without local setup.

### Get started with the desktop app
**Path:** `/desktop-quickstart.md`
**Summary:** Install Claude Code on desktop and start your first coding session

### Get structured output from agents
**Path:** `/agent-sdk/structured-outputs.md`
**Summary:** Return validated JSON from agent workflows using JSON Schema, Zod, or Pydantic. Get type-safe, structured data after multi-turn tool use.

### Give Claude custom tools
**Path:** `/agent-sdk/custom-tools.md`
**Summary:** Define custom tools with the Claude Agent SDK's in-process MCP server so Claude can call your functions, hit your APIs, and perform domain-specific operations.

### Glossary
**Path:** `/glossary.md`
**Summary:** Definitions for Claude Code terminology. Learn what agentic loop, compaction, CLAUDE.md, hooks, subagents, MCP, and other core concepts mean.

### Handle approvals and user input
**Path:** `/agent-sdk/user-input.md`
**Summary:** Surface Claude's approval requests and clarifying questions to users, then return their decisions to the SDK.

### Hooks reference
**Path:** `/hooks.md`
**Summary:** Reference for Claude Code hook events, configuration schema, JSON input/output formats, exit codes, async hooks, HTTP hooks, prompt hooks, and MCP tool hooks.

### Hosting the Agent SDK
**Path:** `/agent-sdk/hosting.md`
**Summary:** Deploy and host Claude Agent SDK in production environments

### How Claude Code uses prompt caching
**Path:** `/prompt-caching.md`
**Summary:** Claude Code manages prompt caching automatically. See why a model switch triggers a slow uncached turn, what `/compact` costs, why CLAUDE.md edits don't apply mid-session, and how to check your cache hit rate.

### How Claude Code works
**Path:** `/how-claude-code-works.md`
**Summary:** Understand the agentic loop, built-in tools, and how Claude Code interacts with your project.

### How Claude remembers your project
**Path:** `/memory.md`
**Summary:** Give Claude persistent instructions with CLAUDE.md files, and let Claude accumulate learnings automatically with auto memory.

### How the agent loop works
**Path:** `/agent-sdk/agent-loop.md`
**Summary:** Understand the message lifecycle, tool execution, context window, and architecture that power your SDK agents.

### Interactive mode
**Path:** `/interactive-mode.md`
**Summary:** Complete reference for keyboard shortcuts, input modes, and interactive features in Claude Code sessions.

### Intercept and control agent behavior with hooks
**Path:** `/agent-sdk/hooks.md`
**Summary:** Intercept and customize agent behavior at key execution points with hooks

### JetBrains IDEs
**Path:** `/jetbrains.md`
**Summary:** Use Claude Code with JetBrains IDEs including IntelliJ, PyCharm, WebStorm, and more

### Keep Claude working toward a goal
**Path:** `/goal.md`
**Summary:** Set a completion condition with /goal and Claude keeps working across turns until the condition is met.

### Launch sessions from links
**Path:** `/deep-links.md`
**Summary:** Open a Claude Code terminal session from a URL. Embed `claude-cli://` links in runbooks, alerts, and dashboards so a click opens Claude Code in the right repo with the right prompt.

### Legal and compliance
**Path:** `/legal-and-compliance.md`
**Summary:** Legal agreements, compliance certifications, and security information for Claude Code.

### Let Claude use your computer from the CLI
**Path:** `/computer-use.md`
**Summary:** Enable computer use in the Claude Code CLI so Claude can open apps, click, type, and see your screen on macOS. Test native apps, debug visual issues, and automate GUI-only tools without leaving your terminal.

### LLM gateway configuration
**Path:** `/llm-gateway.md`
**Summary:** Learn how to configure Claude Code to work with LLM gateway solutions. Covers gateway requirements, authentication configuration, model selection, and provider-specific endpoint setup.

### Manage costs effectively
**Path:** `/costs.md`
**Summary:** Track token usage, set team spend limits, and reduce Claude Code costs with context management, model selection, extended thinking settings, and preprocessing hooks.

### Manage multiple agents with agent view
**Path:** `/agent-view.md`
**Summary:** Dispatch and manage many Claude Code sessions from one screen. Agent view shows what every session is doing and which ones need your input.

### Manage sessions
**Path:** `/sessions.md`
**Summary:** Name, resume, branch, and switch between Claude Code conversations. Covers `--continue`, `--resume`, `--from-pr`, the `/resume` picker, session naming, and where transcripts are stored.

### Migrate to Claude Agent SDK
**Path:** `/agent-sdk/migration-guide.md`
**Summary:** Guide for migrating the Claude Code TypeScript and Python SDKs to the Claude Agent SDK

### Model configuration
**Path:** `/model-config.md`
**Summary:** Learn about the Claude Code model configuration, including model aliases like `opusplan`

### Modifying system prompts
**Path:** `/agent-sdk/modifying-system-prompts.md`
**Summary:** Choose between the `claude_code` preset and a custom system prompt, and customize behavior with CLAUDE.md, output styles, append, or a fully custom prompt.

### Monitoring
**Path:** `/monitoring-usage.md`
**Summary:** Learn how to enable and configure OpenTelemetry for Claude Code.

### Observability with OpenTelemetry
**Path:** `/agent-sdk/observability.md`
**Summary:** Export traces, metrics, and events from the Agent SDK to your observability backend using OpenTelemetry.

### Orchestrate teams of Claude Code sessions
**Path:** `/agent-teams.md`
**Summary:** Coordinate multiple Claude Code instances working together as a team, with shared tasks, inter-agent messaging, and centralized management.

### Output styles
**Path:** `/output-styles.md`
**Summary:** Adapt Claude Code for uses beyond software engineering

### Overview
**Path:** `/overview.md`
**Summary:** Claude Code is an agentic coding tool that reads your codebase, edits files, runs commands, and integrates with your development tools. Available in your terminal, IDE, desktop app, and browser.

### Persist sessions to external storage
**Path:** `/agent-sdk/session-storage.md`
**Summary:** Mirror session transcripts to S3, Redis, or your own backend so any host can resume them.

### Plan in the cloud with ultraplan
**Path:** `/ultraplan.md`
**Summary:** Start a plan from your CLI, draft it on Claude Code on the web, then execute it remotely or back in your terminal

### Platforms and integrations
**Path:** `/platforms.md`
**Summary:** Choose where to run Claude Code and what to connect it to. Compare the CLI, Desktop, VS Code, JetBrains, web, mobile, and integrations like Chrome, Slack, and CI/CD.

### Plugins in the SDK
**Path:** `/agent-sdk/plugins.md`
**Summary:** Load custom plugins to extend Claude Code with commands, agents, skills, and hooks through the Agent SDK

### Plugins reference
**Path:** `/plugins-reference.md`
**Summary:** Complete technical reference for Claude Code plugin system, including schemas, CLI commands, and component specifications.

### Prompt library
**Path:** `/prompt-library.md`
**Summary:** Copy-paste prompts for Claude Code, tagged by task and role.

### Push events into a running session with channels
**Path:** `/channels.md`
**Summary:** Use channels to push messages, alerts, and webhooks into your Claude Code session from an MCP server. Forward CI results, chat messages, and monitoring events so Claude can react while you're away.

### Quickstart
**Path:** `/agent-sdk/quickstart.md`
**Summary:** Get started with the Python or TypeScript Agent SDK to build AI agents that work autonomously

### Quickstart
**Path:** `/quickstart.md`
**Summary:** Welcome to Claude Code!

### Recommend your plugin from your CLI
**Path:** `/plugin-hints.md`
**Summary:** Emit a one-line marker from your CLI so Claude Code prompts users to install your official plugin.

### Rewind file changes with checkpointing
**Path:** `/agent-sdk/file-checkpointing.md`
**Summary:** Track file changes during agent sessions and restore files to any previous state

### Run agents in parallel
**Path:** `/agents.md`
**Summary:** Compare the ways Claude Code can take on multiple tasks at once: subagents, agent view, agent teams, and isolated worktree sessions.

### Run Claude Code programmatically
**Path:** `/headless.md`
**Summary:** Use the Agent SDK to run Claude Code programmatically from the CLI, Python, or TypeScript.

### Run parallel sessions with worktrees
**Path:** `/worktrees.md`
**Summary:** Isolate parallel Claude Code sessions in separate git worktrees so changes don't collide. Covers the `--worktree` flag, subagent isolation, `.worktreeinclude`, cleanup, and non-git VCS hooks.

### Run prompts on a schedule
**Path:** `/scheduled-tasks.md`
**Summary:** Use /loop and the cron scheduling tools to run prompts repeatedly, poll for status, or set one-time reminders within a Claude Code session.

### Sandboxing
**Path:** `/sandboxing.md`
**Summary:** Learn how Claude Code's sandboxed bash tool provides filesystem and network isolation for safer, more autonomous agent execution.

### Scale to many tools with tool search
**Path:** `/agent-sdk/tool-search.md`
**Summary:** Scale your agent to thousands of tools by discovering and loading only what's needed, on demand.

### Schedule recurring tasks in Claude Code Desktop
**Path:** `/desktop-scheduled-tasks.md`
**Summary:** Set up scheduled tasks in Claude Code Desktop to run Claude automatically on a recurring basis for daily code reviews, dependency audits, or morning briefings.

### Securely deploying AI agents
**Path:** `/agent-sdk/secure-deployment.md`
**Summary:** A guide to securing Claude Code and Agent SDK deployments with isolation, credential management, and network controls

### Security
**Path:** `/security.md`
**Summary:** Learn about Claude Code's security safeguards and best practices for safe usage.

### Set up Claude Code for your organization
**Path:** `/admin-setup.md`
**Summary:** A decision map for administrators deploying Claude Code, covering API providers, managed settings, policy enforcement, usage monitoring, and data handling.

### Slash Commands in the SDK
**Path:** `/agent-sdk/slash-commands.md`
**Summary:** Learn how to use slash commands to control Claude Code sessions through the SDK

### Speed up responses with fast mode
**Path:** `/fast-mode.md`
**Summary:** Get faster Opus responses in Claude Code by toggling fast mode.

### Stream responses in real-time
**Path:** `/agent-sdk/streaming-output.md`
**Summary:** Get real-time responses from the Agent SDK as text and tool calls stream in

### Streaming Input
**Path:** `/agent-sdk/streaming-vs-single-mode.md`
**Summary:** Understanding the two input modes for Claude Agent SDK and when to use each

### Subagents in the SDK
**Path:** `/agent-sdk/subagents.md`
**Summary:** Define and invoke subagents to isolate context, run tasks in parallel, and apply specialized instructions in your Claude Agent SDK applications.

### Todo Lists
**Path:** `/agent-sdk/todo-tracking.md`
**Summary:** Track and display todos using the Claude Agent SDK for organized task management

### Tools reference
**Path:** `/tools-reference.md`
**Summary:** Complete reference for the tools Claude Code can use, including permission requirements and per-tool behavior.

### Track cost and usage
**Path:** `/agent-sdk/cost-tracking.md`
**Summary:** Learn how to track token usage, estimate costs, and configure prompt caching with the Claude Agent SDK.

### Track team usage with analytics
**Path:** `/analytics.md`
**Summary:** View Claude Code usage metrics, track adoption, and measure engineering velocity in the analytics dashboard.

### Troubleshoot installation and login
**Path:** `/troubleshoot-install.md`
**Summary:** Fix command not found, PATH, permission, network, and authentication errors when installing or signing in to Claude Code.

### Troubleshooting
**Path:** `/troubleshooting.md`
**Summary:** Fix high CPU or memory usage, hangs, auto-compact thrashing, and search problems in Claude Code, and find the right page for other issues.

### TypeScript SDK V2 session API (removed)
**Path:** `/agent-sdk/typescript-v2-preview.md`
**Summary:** Reference for the removed V2 TypeScript Agent SDK session API, with session-based send/stream patterns for multi-turn conversations.

### Use Claude Code features in the SDK
**Path:** `/agent-sdk/claude-code-features.md`
**Summary:** Load project instructions, skills, hooks, and other Claude Code features into your SDK agents.

### Use Claude Code in VS Code
**Path:** `/vs-code.md`
**Summary:** Install and configure the Claude Code extension for VS Code. Get AI coding assistance with inline diffs, @-mentions, plan review, and keyboard shortcuts.

### Use Claude Code on the web
**Path:** `/claude-code-on-the-web.md`
**Summary:** Configure cloud environments, setup scripts, network access, and Docker in Anthropic's sandbox. Move sessions between web and terminal with `--remote` and `--teleport`.

### Use Claude Code with Chrome (beta)
**Path:** `/chrome.md`
**Summary:** Connect Claude Code to your Chrome browser to test web apps, debug with console logs, automate form filling, and extract data from web pages.

### Voice dictation
**Path:** `/voice-dictation.md`
**Summary:** Speak your prompts in the Claude Code CLI with hold-to-record or tap-to-record voice dictation.

### Week 13 · March 23–27, 2026
**Path:** `/whats-new/2026-w13.md`
**Summary:** Auto mode for hands-off permissions, computer use built in, PR auto-fix in the cloud, transcript search, and a PowerShell tool for Windows.

### Week 14 · March 30 – April 3, 2026
**Path:** `/whats-new/2026-w14.md`
**Summary:** Computer use in the CLI, interactive in-product lessons, flicker-free rendering, per-tool MCP result-size overrides, and plugin executables on PATH.

### Week 15 · April 6–10, 2026
**Path:** `/whats-new/2026-w15.md`
**Summary:** Ultraplan cloud planning, the Monitor tool with self-pacing /loop, /team-onboarding for packaging your setup, and /autofix-pr from your terminal.

### Week 16 · April 13–17, 2026
**Path:** `/whats-new/2026-w16.md`
**Summary:** Claude Opus 4.7 with the new xhigh effort level, Routines on Claude Code on the web, mobile push notifications that ping your phone when Claude needs you, a /usage breakdown that shows what's driving your limits, and native binaries replacing the bundled JavaScript.

### Week 17 · April 20–24, 2026
**Path:** `/whats-new/2026-w17.md`
**Summary:** /ultrareview opens as a research preview, automatic session recaps when you return to a terminal, custom color themes you can build and ship in plugins, and a redesigned Claude Code on the web.

### Week 18 · April 27 – May 1, 2026
**Path:** `/whats-new/2026-w18.md`
**Summary:** Claude Code on Windows runs without Git Bash, claude auth login accepts a pasted OAuth code when the browser callback can't reach localhost, claude project purge cleans up local state per project, and pasting a PR URL into /resume finds the session that created it.

### Week 19 · May 4–8, 2026
**Path:** `/whats-new/2026-w19.md`
**Summary:** Load plugins from .zip archives and URLs, search command history across every project with Ctrl+R, branch new worktrees from local HEAD or the remote default, and block actions unconditionally with auto mode hard deny rules.

### Week 20 · May 11–15, 2026
**Path:** `/whats-new/2026-w20.md`
**Summary:** Manage every Claude Code session from one screen with agent view, keep Claude working toward a goal until a condition holds, and run fast mode on Opus 4.7 by default.

### What's new
**Path:** `/whats-new/index.md`
**Summary:** A weekly digest of notable Claude Code features, with code snippets, demos, and context on why they matter.

### Work with sessions
**Path:** `/agent-sdk/sessions.md`
**Summary:** How sessions persist agent conversation history, and when to use continue, resume, and fork to return to a prior run.

### Zero data retention
**Path:** `/zero-data-retention.md`
**Summary:** Learn about Zero Data Retention (ZDR) for Claude Code on Claude for Enterprise, including scope, disabled features, and how to request enablement.

════════════════════════════════════════════════════════════════════════════════
## Search Patterns

Use these grep patterns to find content in `cli-full-docs.txt`:

```bash
# Find a specific page
grep -A 100 "^PAGE: /path" cli-full-docs.txt

# Extract a complete page (between separators)
sed -n "/^PAGE: \/your-page$/,/^\xe2\x95\x90\{80\}$/p" cli-full-docs.txt

# Search for a keyword across all docs
grep -n "keyword" cli-full-docs.txt
```
