# Warp Terminal Documentation Index

Organized reference for finding topics.
Use grep on `full-docs.txt` for full content.

## Sections Overview

| Section | Pages | Description |
|---------|-------|-------------|
| [AGENT-PLATFORM](#agent-platform) | 91 | Documentation section |
| [API](#api) | 1 | Documentation section |
| [CHANGELOG](#changelog) | 7 | Documentation section |
| [CODE](#code) | 9 | Code editing, review, and codebase context features |
| [ENTERPRISE](#enterprise) | 17 | Documentation section |
| [GETTING-STARTED](#getting-started) | 13 | Installation, setup, keyboard shortcuts, and shell configuration |
| [GUIDES](#guides) | 55 | Documentation section |
| [HOME](#home) | 1 | Documentation section |
| [KNOWLEDGE-AND-COLLABORATION](#knowledge-and-collaboration) | 11 | Warp Drive, notebooks, workflows, teams, and sharing |
| [QUICKSTART](#quickstart) | 1 | Documentation section |
| [REFERENCE](#reference) | 33 | Documentation section |
| [SUPPORT-AND-COMMUNITY](#support-and-community) | 23 | Documentation section |
| [TERMINAL](#terminal) | 71 | Terminal features: blocks, input, output, tabs, themes, and more |

════════════════════════════════════════════════════════════════════════════════
## AGENT-PLATFORM

**91 pages in this section:**

### Agents overview
**Path:** `/agent-platform`
**Summary:** Oz is the orchestration platform for cloud agents, powering both interactive and autonomous agents for development workflows.

### Agent Memory (Research Preview)
**Path:** `/agent-platform/agent-memory`
**Summary:** Agent Memory gives agents in Oz persistent memory across supported harnesses, including the Warp Agent, Claude Code, and Codex.

### Capabilities overview
**Path:** `/agent-platform/capabilities`
**Summary:** Core capabilities and configuration options that shape how agents behave, what context they have access to, and how they execute tasks.

### Agent Notifications
**Path:** `/agent-platform/capabilities/agent-notifications`
**Summary:** Warp surfaces notifications from coding agents, both in-app and via desktop alerts, so you know exactly when an agent needs your attention.

### Profiles & Permissions
**Path:** `/agent-platform/capabilities/agent-profiles-permissions`
**Summary:** Agent Profiles let you customize how your Agent behaves, from its models and autonomy to the tools and permissions it can use.

### Codebase Context
**Path:** `/agent-platform/capabilities/codebase-context`
**Summary:** Warp indexes your Git-tracked codebase to help Agents understand your code and generate accurate, context-aware responses. No code is stored on Warp servers.

### Computer use for agents
**Path:** `/agent-platform/capabilities/computer-use`
**Summary:** Let agents interact with desktop GUIs in sandboxed cloud environments for automated UI testing and validation.

### Full Terminal Use
**Path:** `/agent-platform/capabilities/full-terminal-use`
**Summary:** Full Terminal Use means Warp's agents can interact with active terminal apps to monitor live output and run commands.

### Model Context Protocol (MCP)
**Path:** `/agent-platform/capabilities/mcp`
**Summary:** Configure MCP servers in the Warp desktop app to extend local agents with custom tools and data sources through a standardized interface.

### Agent model choice
**Path:** `/agent-platform/capabilities/model-choice`
**Summary:** Choose from a curated set of top LLMs for Warp's Agents (or let Warp auto-select the best model).

### Agent planning and execution
**Path:** `/agent-platform/capabilities/planning`
**Summary:** Turn requests into structured, editable plans that agents execute step-by-step with version control.

### Rules for agents
**Path:** `/agent-platform/capabilities/rules`
**Summary:** Create reusable Global or Project Rules to ensure Warp’s agents follow your coding standards, project conventions, and personal preferences.

### Skills for agents
**Path:** `/agent-platform/capabilities/skills`
**Summary:** Create reusable instruction sets that teach agents specific tasks and share expertise across your team.

### Slash Commands
**Path:** `/agent-platform/capabilities/slash-commands`
**Summary:** Use Slash Commands in Agent Mode or Auto-Detection Mode to quickly run built-in actions or saved prompts without leaving the input field.

### Agent Task Lists
**Path:** `/agent-platform/capabilities/task-lists`
**Summary:** Track and manage complex Agent workflows with automatic task lists that break requests into clear, actionable steps and update progress in real time.

### Agent web search
**Path:** `/agent-platform/capabilities/web-search`
**Summary:** Warp’s web search lets agents pull in real-time information, documentation, and cited sources whenever it improves an answer.

### Claude Code in Warp
**Path:** `/agent-platform/cli-agents/claude-code`
**Summary:** Set up Claude Code in Warp with full notification support, rich input, code review, and more.

### Codex CLI in Warp
**Path:** `/agent-platform/cli-agents/codex`
**Summary:** Set up Codex in Warp with notification support, rich input, code review, and more.

### OpenCode in Warp
**Path:** `/agent-platform/cli-agents/opencode`
**Summary:** Set up OpenCode in Warp with notification support, rich input, code review, and more.

### Third-party CLI agents overview
**Path:** `/agent-platform/cli-agents/overview`
**Summary:** Warp provides first-class support for third-party CLI coding agents with a rich input editor, notifications, code review, and more.

### Remote Control
**Path:** `/agent-platform/cli-agents/remote-control`
**Summary:** Publish any third-party agent session to the cloud so you can monitor progress, steer the agent, and check in from your phone or another computer.

### Rich input editor
**Path:** `/agent-platform/cli-agents/rich-input`
**Summary:** Warp's rich input editor gives you IDE-style editing, voice input, context attachment, and slash commands for any supported CLI coding agent.

### Agent identities
**Path:** `/agent-platform/cloud-agents/agents`
**Summary:** Agent identities are team-scoped bot accounts that own and execute cloud agent runs. Use them to separate workflows, scope credentials, and attribute automated work.

### Deployment patterns
**Path:** `/agent-platform/cloud-agents/deployment-patterns`
**Summary:** Common architectures for deploying cloud agents, including CLI-only, Oz-hosted, and self-hosted execution patterns.

### Cloud agent environments
**Path:** `/agent-platform/cloud-agents/environments`
**Summary:** Environments ensure your cloud agents run with consistent toolchains across all triggers. Learn when to use environments and how to configure them.

### Cloud Agent FAQs
**Path:** `/agent-platform/cloud-agents/faqs`
**Summary:** Frequently asked questions about cloud agents, including where agents run, how runs work, supported models, security, and common workflows.

### Handoff between local and cloud agents
**Path:** `/agent-platform/cloud-agents/handoff`
**Summary:** Understand how agent handoff moves work between local Warp sessions and cloud agent runs, including what context carries over in each direction.

### Handoff from cloud to cloud
**Path:** `/agent-platform/cloud-agents/handoff/cloud-to-cloud`
**Summary:** Send follow-up instructions to a finished cloud agent run. The run continues with restored workspace state, so the agent picks up where it left off.

### Handoff from local to cloud
**Path:** `/agent-platform/cloud-agents/handoff/local-to-cloud`
**Summary:** Move an in-progress local Warp Agent conversation into a cloud agent run for longer-running work, parallel exploration, or remote follow-up.

### Customizing workspace snapshots
**Path:** `/agent-platform/cloud-agents/handoff/snapshots`
**Summary:** Customize which repositories and files Warp snapshots at the end of a cloud agent run, so handoff continues to work outside the bundled cloud agent image.

### Harnesses in Oz
**Path:** `/agent-platform/cloud-agents/harnesses`
**Summary:** Run Claude Code or Codex as cloud agents. Both inherit the same triggers, environments, secrets, and observability as Warp Agent.

### Third-party cloud agent authentication
**Path:** `/agent-platform/cloud-agents/harnesses/authentication`
**Summary:** Connect your Anthropic or OpenAI credentials to Oz, then launch Claude Code or Codex as cloud agents from the desktop app, Oz web app, or API.

### Claude Code with Oz
**Path:** `/agent-platform/cloud-agents/harnesses/claude-code`
**Summary:** Run Claude Code with Oz. Strong at code review, deep bug investigation, large feature planning, and frontend or UI work.

### Codex with Oz
**Path:** `/agent-platform/cloud-agents/harnesses/codex`
**Summary:** Run Codex with Oz. Strong at codebase migrations, release coordination, batch test generation, and backend or DevOps automation.

### Warp Agent with Oz
**Path:** `/agent-platform/cloud-agents/harnesses/warp-agent`
**Summary:** Warp Agent is Oz's default harness. It routes across leading models, has full terminal access, and is the only harness that can orchestrate subagents.

### Integrations Overview
**Path:** `/agent-platform/cloud-agents/integrations`
**Summary:** Configure Warp's first-party integrations by creating environments, connecting GitHub, and enabling agents to run your code and automate development workflows.

### Azure DevOps integration
**Path:** `/agent-platform/cloud-agents/integrations/azure-devops`
**Summary:** Connect cloud agents to Azure DevOps repos using personal access tokens and Warp-managed secrets.

### Bitbucket integration
**Path:** `/agent-platform/cloud-agents/integrations/bitbucket`
**Summary:** Connect cloud agents to Bitbucket repos using access tokens and Warp-managed secrets.

### Cloud Providers (Preview)
**Path:** `/agent-platform/cloud-agents/integrations/cloud-providers`
**Summary:** Connect cloud agents to your AWS and GCP services.

### Demo: Issue Triage Bot
**Path:** `/agent-platform/cloud-agents/integrations/demo-issue-triage-bot`
**Summary:** A walkthrough demo showing how to trigger a cloud agent from a GitHub Action to automatically triage bug reports and create draft pull requests.

### GitHub Actions
**Path:** `/agent-platform/cloud-agents/integrations/github-actions`
**Summary:** Run agents in GitHub Actions to automate code review, issue triage, and CI fixes.

### GitLab integration
**Path:** `/agent-platform/cloud-agents/integrations/gitlab`
**Summary:** Connect cloud agents to GitLab repos using personal access tokens and Warp-managed secrets.

### Linear integration
**Path:** `/agent-platform/cloud-agents/integrations/linear`
**Summary:** Automate Linear issues with agents that run code in the cloud and create pull requests on your behalf.

### Integrations quickstart
**Path:** `/agent-platform/cloud-agents/integrations/quickstart`
**Summary:** Trigger your first agent from Slack in ~15 minutes and get results in-thread.

### GitHub Actions quickstart
**Path:** `/agent-platform/cloud-agents/integrations/quickstart-github-actions`
**Summary:** Set up your first agent in GitHub Actions in ~10 minutes. Run agents as workflow steps to automate code review and issue triage.

### Slack integration
**Path:** `/agent-platform/cloud-agents/integrations/slack`
**Summary:** Trigger agents from Slack to run cloud tasks, track progress, and create pull requests.

### Managing cloud agents
**Path:** `/agent-platform/cloud-agents/managing-cloud-agents`
**Summary:** Monitor and manage cloud agent activity across your team with Warp's centralized management view, including filtering, status tracking, and session inspection.

### MCP Servers for cloud agents
**Path:** `/agent-platform/cloud-agents/mcp`
**Summary:** Connect cloud agents to external tools, APIs, and internal services using MCP servers.

### Multi-agent orchestration
**Path:** `/agent-platform/cloud-agents/orchestration`
**Summary:** Coordinate a parent agent and its direct child agents across local and cloud runs to build supervisor/worker, fan-out, critic, DAG, and swarm workflows on the Oz Platform.

### Running orchestrated agents
**Path:** `/agent-platform/cloud-agents/orchestration/multi-agent-runs`
**Summary:** Start multi-agent orchestrations from the Warp app, the Oz CLI, the Oz web app, or the Oz API, and inspect parent and child conversations and artifacts.

### Cloud agents overview
**Path:** `/agent-platform/cloud-agents/overview`
**Summary:** Run background agents in the cloud from events, schedules, or integrations with team-wide observability.

### Oz web app for cloud agents
**Path:** `/agent-platform/cloud-agents/oz-web-app`
**Summary:** Use the Oz web app to manage cloud agents, view runs, create schedules, and configure environments and integrations from any browser or mobile device.

### Oz Platform overview
**Path:** `/agent-platform/cloud-agents/platform`
**Summary:** The Oz Platform provides the CLI, API/SDK, orchestration, environments, and observability for cloud agents.

### Cloud agents quickstart
**Path:** `/agent-platform/cloud-agents/quickstart`
**Summary:** Learn how to run your first cloud agent in ~10 minutes. Cloud agents run in remote environments, enabling automation, scheduling, and team collaboration.

### Cloud agent secrets
**Path:** `/agent-platform/cloud-agents/secrets`
**Summary:** Securely store, scope, and inject credentials for Warp cloud agents across CLI, Slack, Linear, and scheduled runs—without ever exposing secret values.

### Self-hosting overview
**Path:** `/agent-platform/cloud-agents/self-hosting`
**Summary:** Run cloud agents on your own infrastructure. Choose between a managed worker daemon orchestrated by Oz or unmanaged CLI-based execution you control.

### Managed: Direct backend
**Path:** `/agent-platform/cloud-agents/self-hosting/managed-direct`
**Summary:** Run the Oz managed worker with the Direct backend to execute cloud agent tasks directly on the host, without Docker or Kubernetes.

### Managed: Docker backend
**Path:** `/agent-platform/cloud-agents/self-hosting/managed-docker`
**Summary:** Run the Oz managed worker daemon with the Docker backend to execute cloud agent tasks in isolated containers on your infrastructure.

### Managed: Kubernetes backend
**Path:** `/agent-platform/cloud-agents/self-hosting/managed-kubernetes`
**Summary:** Deploy the Oz managed worker into a Kubernetes cluster with the included Helm chart. Each agent task runs as a Kubernetes Job in your cluster.

### Self-hosted worker monitoring
**Path:** `/agent-platform/cloud-agents/self-hosting/monitoring`
**Summary:** Monitor self-hosted Oz workers with OpenTelemetry metrics. Export to Prometheus, OTLP, or console to track worker health, task throughput, and saturation.

### Self-hosting quickstart
**Path:** `/agent-platform/cloud-agents/self-hosting/quickstart`
**Summary:** Get a managed self-hosted Oz worker running on Docker and route your first cloud agent run to it in under 10 minutes.

### Self-hosted worker reference
**Path:** `/agent-platform/cloud-agents/self-hosting/reference`
**Summary:** Complete reference for the oz-agent-worker daemon — CLI flags and config file schema for the Docker, Kubernetes, and Direct backends.

### Security and networking
**Path:** `/agent-platform/cloud-agents/self-hosting/security-and-networking`
**Summary:** Security model, data boundaries, and network requirements for self-hosted Oz cloud agents — including per-backend considerations and BYOLLM.

### Self-hosting troubleshooting
**Path:** `/agent-platform/cloud-agents/self-hosting/troubleshooting`
**Summary:** Diagnose and fix common problems with self-hosted Oz worker daemons across Docker, Kubernetes, and Direct backends.

### Unmanaged architecture
**Path:** `/agent-platform/cloud-agents/self-hosting/unmanaged`
**Summary:** Run agents in your existing CI, Kubernetes, or dev environments using the oz agent run CLI with Warp tracking and observability.

### Skills as Agents
**Path:** `/agent-platform/cloud-agents/skills-as-agents`
**Summary:** Run agents based on skills for consistent, repeatable workflows. Use skills with local or cloud agents from the CLI, Oz web app, API, or on a schedule.

### Access, billing, and identity permissions
**Path:** `/agent-platform/cloud-agents/team-access-billing-and-identity`
**Summary:** Understand how access to cloud agents works for individuals and teams, how billing and credits apply, and how Warp maps user identities across integrations.

### Triggers overview
**Path:** `/agent-platform/cloud-agents/triggers`
**Summary:** Configure triggers to run cloud agents automatically based on schedules or events.

### Scheduled Agents
**Path:** `/agent-platform/cloud-agents/triggers/scheduled-agents`
**Summary:** Run cloud agents on a cron schedule for automated maintenance and recurring tasks.

### Scheduled Agents quickstart
**Path:** `/agent-platform/cloud-agents/triggers/scheduled-agents-quickstart`
**Summary:** Schedule a cloud agent to run recurring tasks automatically — issue triage, dependency checks, code cleanup, and more.

### Cloud agent session sharing
**Path:** `/agent-platform/cloud-agents/viewing-cloud-agent-runs`
**Summary:** Open, inspect, and steer remote cloud agent runs in real time from Warp or the web.

### Warp-hosted agents
**Path:** `/agent-platform/cloud-agents/warp-hosting`
**Summary:** Run cloud agents on Warp's infrastructure. Warp handles scaling, isolation, and performance for agent execution.

### Agents in Warp
**Path:** `/agent-platform/getting-started/agents-in-warp`
**Summary:** Warp's agents are capable collaborators that help you write code, debug issues, and complete terminal workflows, all from natural language prompts.

### Agent platform FAQs
**Path:** `/agent-platform/getting-started/faqs`
**Summary:** Frequently asked questions about Warp's AI features, including supported models, privacy practices, credit limits, billing, and usage guidelines.

### Active AI Recommendations
**Path:** `/agent-platform/local-agents/active-ai`
**Summary:** Active AI Recommendations proactively suggest fixes and next actions based on your command line errors, inputs, and outputs.

### Agent context overview
**Path:** `/agent-platform/local-agents/agent-context`
**Summary:** How to attach various forms of multi-modal context directly to Warp's Agent within a prompt.

### Blocks as Context
**Path:** `/agent-platform/local-agents/agent-context/blocks-as-context`
**Summary:** Attach blocks from your terminal as context so Warp’s Agent can understand errors, outputs, or previous commands when responding to your queries.

### Images as Context
**Path:** `/agent-platform/local-agents/agent-context/images-as-context`
**Summary:** Attach screenshots, diagrams, or other images to your prompt so Warp’s Agent can use visual context when generating responses.

### Selection as Context
**Path:** `/agent-platform/local-agents/agent-context/selection-as-context`
**Summary:** Attach text or diffs directly from Warp’s editor or Code Review panel as context for your Agent prompts.

### URLs as Context
**Path:** `/agent-platform/local-agents/agent-context/urls-as-context`
**Summary:** Attach a public URL to your prompt so the agent can reference that page's content.

### Using @ to Add Context
**Path:** `/agent-platform/local-agents/agent-context/using-to-add-context`
**Summary:** Use @ to reference files, folders, code symbols, and Warp Drive objects as agent context.

### Cloud-synced conversations
**Path:** `/agent-platform/local-agents/cloud-conversations`
**Summary:** Sync agent conversations to the cloud to access them across devices, share with teammates, and continue past conversations from anywhere.

### Agent code diffs and review
**Path:** `/agent-platform/local-agents/code-diffs`
**Summary:** How to review, refine, and apply code changes generated by Warp’s Agents with the built-in diff editor in Agent Conversations.

### Generate (Legacy)
**Path:** `/agent-platform/local-agents/generate`
**Summary:** Use natural language to look up commands or input, accessible either directly from the command-line input or inside any interactive command or program.

### Interacting with agents
**Path:** `/agent-platform/local-agents/interacting-with-agents`
**Summary:** Manage agent conversations across sessions with follow-ups, context blocks, and multi-thread support.

### Conversation Forking
**Path:** `/agent-platform/local-agents/interacting-with-agents/conversation-forking`
**Summary:** Branch into a new agent thread with full context to explore alternatives without altering the original conversation.

### Terminal and Agent modes
**Path:** `/agent-platform/local-agents/interacting-with-agents/terminal-and-agent-modes`
**Summary:** Warp provides two distinct modes: a clean terminal for commands, and a dedicated conversation view for multi-turn agent workflows.

### Voice input for agents
**Path:** `/agent-platform/local-agents/interacting-with-agents/voice`
**Summary:** Voice enables natural language interaction with Warp, letting you speak commands and queries directly to your terminal.

### Interactive Code Review
**Path:** `/agent-platform/local-agents/interactive-code-review`
**Summary:** Review agent-generated code, leave inline comments, and have Warp's native agent or any supported third-party CLI agent apply your feedback.

### Warp Agents overview
**Path:** `/agent-platform/local-agents/overview`
**Summary:** Powerful AI features like agents, code review, voice, and active AI recommendations, fully integrated into the Warp Agentic Development Environment.

### Agent Session Sharing
**Path:** `/agent-platform/local-agents/session-sharing`
**Summary:** Share live agent sessions so collaborators can view, steer, and interact with agent activity from any device — in real time or asynchronously.


════════════════════════════════════════════════════════════════════════════════
## API

**1 pages in this section:**

### <!DOCTYPE html><html lang="en" class="astro-gtzdsgas"> <head><meta charset="utf-
**Path:** `/api`


════════════════════════════════════════════════════════════════════════════════
## CHANGELOG

**7 pages in this section:**

### Changelog
**Path:** `/changelog`
**Summary:** Warp ships weekly updates, typically on Thursdays.

### Changelog — 2021
**Path:** `/changelog/2021`
**Summary:** Warp release notes for 2021. Updates ship weekly, typically on Thursdays.

### Changelog — 2022
**Path:** `/changelog/2022`
**Summary:** Warp release notes for 2022. Updates ship weekly, typically on Thursdays.

### Changelog — 2023
**Path:** `/changelog/2023`
**Summary:** Warp release notes for 2023. Updates ship weekly, typically on Thursdays.

### Changelog — 2024
**Path:** `/changelog/2024`
**Summary:** Warp release notes for 2024. Updates ship weekly, typically on Thursdays.

### Changelog — 2025
**Path:** `/changelog/2025`
**Summary:** Warp release notes for 2025. Updates ship weekly, typically on Thursdays.

### Changelog — 2026
**Path:** `/changelog/2026`
**Summary:** Warp release notes for 2026. Updates ship weekly, typically on Thursdays.


════════════════════════════════════════════════════════════════════════════════
## CODE
*Code editing, review, and codebase context features*

**9 pages in this section:**

### Built-in Code Editor
**Path:** `/code/code-editor`
**Summary:** Make in-context code edits with Warp's built-in editor, featuring syntax highlighting, tabs, and Vim keybindings.

### Code Editor Vim Keybindings
**Path:** `/code/code-editor/code-editor-vim-keybindings`
**Summary:** Use Vim keybindings in Warp's code editor for keyboard-driven navigation and editing.

### File Tree (Project Explorer)
**Path:** `/code/code-editor/file-tree`
**Summary:** Browse, open, and manage project files with Warp's native file tree and context menu actions.

### Find and Replace
**Path:** `/code/code-editor/find-and-replace`
**Summary:** Search and replace text in Warp's code editor with regex, case sensitivity, and smart case preservation.

### Language Server Protocol (LSP)
**Path:** `/code/code-editor/language-server-protocol`
**Summary:** Get hover info, go-to-definition, diagnostics, and format-on-save via built-in LSP support.

### Code Review panel
**Path:** `/code/code-review`
**Summary:** The Code Review panel lets you review, edit, and manage Git diffs in real time, with options to attach, revert, or open files directly.

### Git worktrees
**Path:** `/code/git-worktrees`
**Summary:** Warp natively supports Git worktrees, letting you work on multiple branches simultaneously with full Code Review, Codebase Context, and Agent support.

### Code overview
**Path:** `/code/overview`
**Summary:** Generate and edit code with Warp's coding agent, review inline diffs, and apply changes across your codebase.

### Feature support over SSH
**Path:** `/code/ssh-feature-support`
**Summary:** A reference for which Warp coding features are available over SSH and which are limited to local sessions.


════════════════════════════════════════════════════════════════════════════════
## ENTERPRISE

**17 pages in this section:**

### Enterprise overview
**Path:** `/enterprise`
**Summary:** Warp Enterprise provides the security, control, and collaboration features organizations need to deploy Warp across their engineering teams at scale.

### Enterprise Analytics API
**Path:** `/enterprise/enterprise-features/analytics-api`
**Summary:** Programmatically access team-level usage data for Warp's enterprise plans — per-team summaries, per-user rollups, and message-level activity events.

### Architecture and deployment
**Path:** `/enterprise/enterprise-features/architecture-and-deployment`
**Summary:** Understand Warp's system architecture and choose the right deployment model for your organization - Warp-hosted, self-hosted, or hybrid.

### Bring your own LLM
**Path:** `/enterprise/enterprise-features/bring-your-own-llm`
**Summary:** Route Warp's agents through your AWS Bedrock models for billing control and infrastructure flexibility.

### Enterprise FAQ
**Path:** `/enterprise/getting-started/faq`
**Summary:** Answers to common questions about Warp Enterprise, including login issues, SSO, and getting started.

### Getting started for developers
**Path:** `/enterprise/getting-started/getting-started-developers`
**Summary:** Download Warp, log in to your team, and start using agents, Codebase Context, and collaborative features to accelerate your development workflow.

### Getting started with Warp Enterprise
**Path:** `/enterprise/getting-started/getting-started-enterprise`
**Summary:** Set up Warp Enterprise for your organization with SSO configuration, team management, and admin controls.

### Enterprise quickstart
**Path:** `/enterprise/getting-started/quickstart`
**Summary:** Get up and running with Warp Enterprise in under 10 minutes. Log in, set up your terminal, and run your first agent.

### Security overview
**Path:** `/enterprise/security-and-compliance/security-overview`
**Summary:** Understand Warp's security architecture, data handling practices, and compliance certifications to ensure your organization's requirements are met.

### Single Sign-On (SSO)
**Path:** `/enterprise/security-and-compliance/sso`
**Summary:** Configure Single Sign-On (SSO) to authenticate and manage access to Warp across your organization.

### Warp Trust Center
**Path:** `/enterprise/security-and-compliance/trust-center`
**Summary:** Access Warp's security documentation, compliance certifications, and third-party assessment resources to complete your vendor security review.

### Enterprise billing
**Path:** `/enterprise/support-and-resources/billing`
**Summary:** Learn about billing for Warp Enterprise, including credits, cloud agent costs, and billing management.

### Feedback and feature requests
**Path:** `/enterprise/support-and-resources/feedback-and-feature-requests`
**Summary:** Report bugs, request features, and get support as a Warp Enterprise customer.

### Troubleshooting login
**Path:** `/enterprise/support-and-resources/troubleshooting-login`
**Summary:** Resolve common login and SSO issues for Warp Enterprise users and IT admins.

### Admin Panel for teams
**Path:** `/enterprise/team-management/admin-panel`
**Summary:** Centralized management for team administrators to configure Warp settings, control agent behavior, and enforce security policies across your organization.

### Roles and permissions
**Path:** `/enterprise/team-management/roles-and-permissions`
**Summary:** Understand user roles, permissions, and access controls for managing your Warp Enterprise team.

### Team management in Warp
**Path:** `/enterprise/team-management/teams`
**Summary:** Create and manage teams in Warp to organize users, share resources, and collaborate across your engineering organization.


════════════════════════════════════════════════════════════════════════════════
## GETTING-STARTED
*Installation, setup, keyboard shortcuts, and shell configuration*

**13 pages in this section:**

### Keyboard Shortcuts
**Path:** `/getting-started/keyboard-shortcuts`
**Summary:** View, customize, and remap keyboard shortcuts for all Warp features.

### Migrate to Warp
**Path:** `/getting-started/migrate-to-warp`
**Summary:** Move your settings and mental model into Warp. Pick the tool you're coming from for step-by-step guidance and Warp equivalents.

### Migrate to Warp from Claude Code
**Path:** `/getting-started/migrate-to-warp/migrate-to-warp-from-claude-code`
**Summary:** Keep using Claude Code in Warp — with rich input, code review, and notifications — or switch from Claude Code to Warp's Agent Mode as your primary coding agent.

### Migrate to Warp from Cursor
**Path:** `/getting-started/migrate-to-warp/migrate-to-warp-from-cursor`
**Summary:** Reconfigure your terminal and agent settings when switching to Warp from Cursor, or run Warp alongside Cursor as your agent terminal.

### Migrate to Warp from Ghostty
**Path:** `/getting-started/migrate-to-warp/migrate-to-warp-from-ghostty`
**Summary:** Moving to Warp from Ghostty? Here's how to bring over your themes, fonts, and keybindings, plus where to find Warp's equivalents for Ghostty's native features.

### Migrate to Warp from iTerm2
**Path:** `/getting-started/migrate-to-warp/migrate-to-warp-from-iterm2`
**Summary:** Import your iTerm2 profile into Warp to transfer themes, fonts, keybindings, hotkey windows, and more in a few clicks.

### Migrate to Warp from macOS Terminal
**Path:** `/getting-started/migrate-to-warp/migrate-to-warp-from-macos-terminal`
**Summary:** Switch from the default macOS Terminal app to Warp. Match your setup and discover what Warp adds beyond the basics.

### Migrate to Warp from VS Code terminal
**Path:** `/getting-started/migrate-to-warp/migrate-to-warp-from-vs-code-terminal`
**Summary:** Replicate your VS Code integrated terminal setup in Warp - shell, fonts, keybindings - or run Warp alongside VS Code as a richer terminal.

### Migrate to Warp from Windows Terminal
**Path:** `/getting-started/migrate-to-warp/migrate-to-warp-from-windows-terminal`
**Summary:** Switch from Windows Terminal to Warp on Windows. Reconfigure profiles, shells, fonts, keybindings, and find Warp equivalents.

### Coding in Warp
**Path:** `/getting-started/quickstart/coding-in-warp`
**Summary:** Agents can generate and edit code directly from within Warp.

### Customizing Warp
**Path:** `/getting-started/quickstart/customizing-warp`
**Summary:** A complete guide to customizing Warp: themes, vertical tabs, tab configs, prompt chips, keybindings, AI models, and more.

### Installation and setup
**Path:** `/getting-started/quickstart/installation-and-setup`
**Summary:** Install Warp on macOS, Windows, or Linux. All installation options include auto-update for new features, bug fixes, and performance improvements.

### Supported Shells
**Path:** `/getting-started/supported-shells`
**Summary:** Warp supports bash, zsh, fish, PowerShell, and WSL2 across macOS, Windows, and Linux.


════════════════════════════════════════════════════════════════════════════════
## GUIDES

**55 pages in this section:**

### Guides
**Path:** `/guides`
**Summary:** Step-by-step guides for Warp, the agentic development environment — from first setup to coding agent workflows, MCP integrations, and full app builds.

### How to: Edit Agent Code in Warp
**Path:** `/guides/agent-workflows/how-to-edit-agent-code-in-warp`
**Summary:** Review, edit, and refine AI-generated code diffs directly in Warp — accept, reject, or modify changes before applying them.

### How to: Explain Your Codebase Using Warp (Rust Codebase)
**Path:** `/guides/agent-workflows/how-to-explain-your-codebase-using-warp-rust-codebase`
**Summary:** Use Warp's coding agents with semantic and symbol search to explore, understand, and modify unfamiliar codebases — demonstrated on a large Rust project.

### How to review AI-generated code
**Path:** `/guides/agent-workflows/how-to-review-ai-generated-code`
**Summary:** Review AI-generated code in Warp with visual diffs and inline comments — works with Claude Code, Codex, or any CLI agent.

### How To: Review PRs Like A Senior Dev
**Path:** `/guides/agent-workflows/how-to-review-prs-like-a-senior-dev`
**Summary:** Prompt Warp's coding agent to generate structured PR reviews with risk assessment, critical issues, and merge confidence scoring.

### How To: Run 3 Agents in Parallel
**Path:** `/guides/agent-workflows/how-to-run-3-agents-in-parallel-summarize-logs-analyze-pr-modify-ui`
**Summary:** Run three agent tasks simultaneously in Warp — modify UI, analyze code reviews, and summarize production logs in parallel.

### How to run multiple AI coding agents
**Path:** `/guides/agent-workflows/how-to-run-multiple-ai-coding-agents`
**Summary:** Run Claude Code, Codex, and other AI coding agents in parallel using vertical tabs, tab configs, and notifications to manage multiple sessions at once.

### How to use voice and images to prompt coding agents
**Path:** `/guides/agent-workflows/how-to-use-voice-and-images-to-prompt-coding-agents`
**Summary:** Use voice and image context to prompt coding agents faster in Warp — works with Claude Code, Codex, and any CLI agent.

### Running Multiple Agents At Once With Warp
**Path:** `/guides/agent-workflows/running-multiple-agents-at-once-with-warp`
**Summary:** Run multiple agent tasks simultaneously in Warp — revert PRs, edit shortcuts, and add tests across repos without losing context.

### Understanding Your Codebase
**Path:** `/guides/agent-workflows/understanding-your-codebase`
**Summary:** Use Warp's Codebase Context to search across client and server repos, generate architecture summaries, and onboard to unfamiliar features fast.

### Using Images As Context With Warp
**Path:** `/guides/agent-workflows/using-images-as-context-with-warp`
**Summary:** Attach screenshots and design mockups as context for Warp's agent to generate UI code, debug visual issues, and match Figma designs.

### 5 agent workflows for product managers
**Path:** `/guides/agent-workflows/warp-for-product-managers`
**Summary:** Five agent workflows that automate status updates, documentation, Slack search, and meeting prep for product managers.

### Warp vs Claude Code
**Path:** `/guides/agent-workflows/warp-vs-claude-code`
**Summary:** Compare Warp and Claude Code across setup, diff review, model selection, configuration, and performance.

### Building a Chrome Extension (D3.js + Javascript + HTML + CSS)
**Path:** `/guides/build-an-app-in-warp/building-a-chrome-extension-d3js-javascript-html-css`
**Summary:** Build a D3.js Sankey diagram Chrome extension using Warp — scaffold, debug, coordinate multiple agents, and publish to the Chrome Web Store.

### Building a Real-time Chat App (GitHub MCP + Railway)
**Path:** `/guides/build-an-app-in-warp/building-a-real-time-chat-app-github-mcp-railway`
**Summary:** Build and deploy a real-time chat app with Python, FastAPI, and JavaScript — from idea to production, all inside Warp.

### Building a Slackbot
**Path:** `/guides/build-an-app-in-warp/building-a-slackbot`
**Summary:** Set up a self-hosted Warp Slackbot that answers repo questions and opens PRs directly from Slack using Docker and GitHub integration.

### Building Warp's Input - With Warp
**Path:** `/guides/build-an-app-in-warp/building-warps-input-with-warp`
**Summary:** Watch how a Warp designer uses Warp's own agent to locate, modify, and test a UI component change in a large Rust codebase.

### Creating Rules For Agents
**Path:** `/guides/configuration/creating-rules-for-agents`
**Summary:** Create reusable Rules in Warp to encode team conventions — like Dockerfile patterns or dependency management — so agents follow your standards.

### How To: Configure YOLO and Strategic Agent Profiles
**Path:** `/guides/configuration/how-to-configure-yolo-and-strategic-agent-profiles`
**Summary:** Configure custom agent profiles in Warp to control planning depth, autonomy, and execution speed — demonstrated with YOLO and Strategic examples.

### How To: Create Project Rules for an Existing Project
**Path:** `/guides/configuration/how-to-create-project-rules-for-an-existing-project-astro-typescript-tailwind`
**Summary:** Create and maintain an AGENTS.md project rules file so coding agents always understand your project's setup, commands, architecture, and conventions.

### How To: Set Coding Best Practices
**Path:** `/guides/configuration/how-to-set-coding-best-practices`
**Summary:** Use Warp Rules to enforce coding style, TypeScript conventions, and documentation quality across AI-generated code.

### How To: Set Coding Preferences with Rules
**Path:** `/guides/configuration/how-to-set-coding-preferences-with-rules`
**Summary:** Store your package manager, environment tool, and CLI preferences as Warp Rules so agents automatically use pnpm, miniconda, or your preferred tools.

### How To: Set Tech Stack Preferences with Rules
**Path:** `/guides/configuration/how-to-set-tech-stack-preferences-with-rules`
**Summary:** Define your preferred frameworks and tech stack in Warp Rules so agents consistently use Astro, SvelteKit, Vite, or your tools of choice.

### How to set up self-serve data analytics with Skills
**Path:** `/guides/configuration/how-to-set-up-self-serve-data-analytics-with-skills`
**Summary:** Set up a self-serve data analytics workflow in Warp using two community Skills that map questions to dbt models and structure reproducible analyses.

### How To: Sync Your Monorepos
**Path:** `/guides/configuration/how-to-sync-your-monorepos`
**Summary:** Define global Rules in Warp to keep monorepo schemas, server types, and client types automatically synchronized across repositories.

### How To: Use Agent Profiles Efficiently
**Path:** `/guides/configuration/how-to-use-agent-profiles-efficiently`
**Summary:** Compare Strategic and YOLO agent profiles side-by-side to choose the right balance of planning, safety, and speed for your project.

### Trigger Reusable Actions With Saved Prompts
**Path:** `/guides/configuration/trigger-reusable-actions-with-saved-prompts`
**Summary:** Save and share prompts in Warp Drive to automate commits, code reviews, and PR creation across your team.

### How to: Analyze Cloud Run Logs (gcloud)
**Path:** `/guides/devops/how-to-analyze-cloud-run-logs-gcloud`
**Summary:** Use Warp to pull, organize, and analyze Cloud Run production logs by severity with natural language prompts and automated Python scripts.

### How To: Create a Production Ready Docker Setup
**Path:** `/guides/devops/how-to-create-a-production-ready-docker-setup`
**Summary:** Use Agents in Warp to generate optimized Dockerfiles, docker-compose configs, and .dockerignore files for multi-stage production deployments.

### How To: Create Priority Matrix for Database Optimization
**Path:** `/guides/devops/how-to-create-priority-matrix-for-database-optimization`
**Summary:** Prompt Warp to audit SQL queries, analyze execution plans, and generate a priority matrix ranking database optimizations by impact and effort.

### How to: Generate Unit and Security Tests to Debug Faster
**Path:** `/guides/devops/how-to-generate-unit-and-security-tests-to-debug-faster`
**Summary:** Prompt Warp to generate comprehensive unit and security tests for REST APIs, including SQL injection, XSS, and auth validation checks.

### How To: Prevent Secrets from Leaking
**Path:** `/guides/devops/how-to-prevent-secrets-from-leaking`
**Summary:** Use Warp Rules and built-in secret reduction to prevent API keys and credentials from leaking in agent output, demos, and shared sessions.

### How To: Write SQL Commands inside a Postgres REPL
**Path:** `/guides/devops/how-to-write-sql-commands-inside-a-postgres-repl`
**Summary:** Use Agents in Warp inside a Postgres REPL to translate natural language into SQL queries — works with Node.js, Python, and MySQL too.

### Improve Your Kubernetes Workflow (kubectl + helm)
**Path:** `/guides/devops/improve-your-kubernetes-workflow-kubectl-helm`
**Summary:** Streamline kubectl and Helm workflows with Warp's AI assistance, active suggestions, custom workflows, and synchronized panes.

### Context7 MCP: Update Astro Project with Best Practices
**Path:** `/guides/external-tools/context7-mcp-update-astro-project-with-best-practices`
**Summary:** Use the Context7 MCP server to give Warp agents real-time access to framework documentation for automated project upgrades.

### Figma Remote MCP: Create a Website from a Figma File
**Path:** `/guides/external-tools/figma-remote-mcp-create-a-website-from-a-figma-file-from-scratch`
**Summary:** Connect Warp to Figma's remote MCP server via OAuth and generate front-end code directly from your design files.

### GitHub MCP: Summarizing Open PRs & Creating GH Issues
**Path:** `/guides/external-tools/github-mcp-summarizing-open-prs-and-creating-gh-issues`
**Summary:** Connect the GitHub MCP server to Warp to summarize open PRs, create issues from TODO comments, and automate repo management.

### How to set up Claude Code
**Path:** `/guides/external-tools/how-to-set-up-claude-code`
**Summary:** Set up Claude Code in Warp, configure it for your project, and learn productivity tips — from voice prompting to visual code review.

### How to set up Codex CLI
**Path:** `/guides/external-tools/how-to-set-up-codex-cli`
**Summary:** Set up OpenAI's Codex CLI in Warp, configure it for your project, and learn productivity tips for faster AI-assisted coding workflows in Warp.

### How to set up Gemini CLI
**Path:** `/guides/external-tools/how-to-set-up-gemini-cli`
**Summary:** Set up Google's Gemini CLI in Warp, configure it for your project, and learn productivity tips for faster AI-assisted coding workflows.

### How To Set Up Ollama
**Path:** `/guides/external-tools/how-to-set-up-ollama`
**Summary:** Install Ollama, run LLMs locally, compare model performance, and integrate local models into your apps using Warp.

### How to set up OpenCode
**Path:** `/guides/external-tools/how-to-set-up-opencode`
**Summary:** Set up OpenCode in Warp, configure it for your project, and learn productivity tips for faster AI-assisted coding workflows.

### Linear MCP: Retrieve issue data
**Path:** `/guides/external-tools/linear-mcp-retrieve-issue-data`
**Summary:** Add the Linear MCP server to Warp and query your issues, tasks, and assignments directly from the terminal.

### Linear MCP: Updating Tickets with a Lean Build Approach
**Path:** `/guides/external-tools/linear-mcp-updating-tickets-with-a-lean-build-approach`
**Summary:** Use Warp's Linear MCP integration to update ticket descriptions, propagate changes to subtasks, and maintain a lean build strategy.

### Puppeteer MCP: Scraping Amazon Web Reviews
**Path:** `/guides/external-tools/puppeteer-mcp-scraping-amazon-web-reviews`
**Summary:** Configure the Puppeteer MCP server in Warp to automate browser tasks like navigating sites, scraping product data, and analyzing reviews.

### Sentry MCP: Fix Sentry Error in Empower Website
**Path:** `/guides/external-tools/sentry-mcp-fix-sentry-error-in-empower-website`
**Summary:** Connect the Sentry MCP server to Warp, fetch live error data, diagnose stack traces, and auto-generate fixes for production issues.

### SQLite and Stripe MCP: Basic Queries You Can Make After Set Up
**Path:** `/guides/external-tools/sqlite-and-stripe-mcp-basic-queries-you-can-make-after-set-up`
**Summary:** Connect SQLite and Stripe MCP servers to Warp and run conversational queries against your local database and payment data.

### Using MCP Servers with Warp
**Path:** `/guides/external-tools/using-mcp-servers-with-warp`
**Summary:** Connect MCP servers to Warp's agent, add Rules for automatic tool selection, and resolve tickets using external systems like Linear.

### How To: Code UI That Matches Your Mockup
**Path:** `/guides/frontend/how-to-actually-code-ui-that-matches-your-mockup-react-tailwind`
**Summary:** Prompt Warp to generate pixel-perfect React + Tailwind code from design mockups, with structured specs and iterative refinement.

### How To: Replace A UI Element in Warp (Rust Codebase)
**Path:** `/guides/frontend/how-to-replace-a-ui-element-in-warp-rust-codebase`
**Summary:** Use Agent Mode in Warp to plan and execute icon replacements across a large Rust codebase — with live diffs, auto-compilation, and self-correction.

### 10 Coding Features You Should Know
**Path:** `/guides/getting-started/10-coding-features-you-should-know`
**Summary:** Discover 10 essential coding features in Warp — file search, tabbed editor, find and replace, syntax highlighting, code review panel, and more.

### How to: Customize Warp's Appearance
**Path:** `/guides/getting-started/how-to-customize-warps-appearance`
**Summary:** Customize Warp's themes, input placement, AI settings, codebase indexing, team collaboration, and visual appearance to fit your workflow.

### How to Make Warp’s UI More Minimal
**Path:** `/guides/getting-started/how-to-make-warps-ui-more-minimal`
**Summary:** Reduce visual noise in Warp by disabling UI elements, switching to a minimal theme, using the classic prompt, and hiding the tab bar.

### How To Master Warp's Code Review Panel
**Path:** `/guides/getting-started/how-to-master-warps-code-review-panel`
**Summary:** Use Warp's Code Review Panel to view file diffs, edit code inline, componentize changes, and commit directly — all without leaving the terminal.

### Welcome to Warp
**Path:** `/guides/getting-started/welcome-to-warp`
**Summary:** Get oriented with Warp's agentic terminal. Learn the basics of prompt-based coding, blending terminal and agent workflows, and navigating the interface.


════════════════════════════════════════════════════════════════════════════════
## HOME

**1 pages in this section:**

### <!DOCTYPE html><html lang="en" dir="ltr" data-theme="dark" data-has-toc data-has
**Path:** `/`
**Summary:** Warp is where you work — a fast, modern terminal built for coding with agents.


════════════════════════════════════════════════════════════════════════════════
## KNOWLEDGE-AND-COLLABORATION
*Warp Drive, notebooks, workflows, teams, and sharing*

**11 pages in this section:**

### Team Admin Panel
**Path:** `/knowledge-and-collaboration/admin-panel`
**Summary:** Centralized management for team administrators to configure workspace settings enforced across all team members.

### Session Sharing
**Path:** `/knowledge-and-collaboration/session-sharing`
**Summary:** Share terminal sessions with teammates for collaboration, debugging, and knowledge sharing.

### Team management
**Path:** `/knowledge-and-collaboration/teams`
**Summary:** Create or join a team to collaborate with others in Warp.

### Warp Drive overview
**Path:** `/knowledge-and-collaboration/warp-drive`
**Summary:** Warp Drive is a workspace in your terminal where you can save Workflows, Notebooks, Prompts, and Environment Variables for personal use or to share with a team.

### Agent Mode Context
**Path:** `/knowledge-and-collaboration/warp-drive/agent-mode-context`
**Summary:** Agents use your Warp Drive content—Workflows, Notebooks, Rules, MCP Servers, and Environment Variables—for context-aware responses.

### AI-Integrated Objects
**Path:** `/knowledge-and-collaboration/warp-drive/ai-objects`
**Summary:** Access Rules, MCP Servers, Skills, and Prompts in Warp Drive to give agents personalized context.

### Environment variables
**Path:** `/knowledge-and-collaboration/warp-drive/environment-variables`
**Summary:** Save or sync environment variables to load into your terminal sessions.

### Warp Drive Notebooks
**Path:** `/knowledge-and-collaboration/warp-drive/notebooks`
**Summary:** Save interactive playbooks to simplify onboarding and development.

### Warp Drive prompts
**Path:** `/knowledge-and-collaboration/warp-drive/prompts`
**Summary:** Save and reuse parameterized Agent Mode prompts to run on-demand.

### Warp Drive on the web
**Path:** `/knowledge-and-collaboration/warp-drive/web`
**Summary:** Access your Warp Drive objects and shared sessions from any browser or touch screen device, including mobile phones, tablets, and touch-enabled laptops.

### Warp Drive Workflows
**Path:** `/knowledge-and-collaboration/warp-drive/workflows`
**Summary:** Save parameterized commands as Workflows and execute them on-demand from Warp Drive.


════════════════════════════════════════════════════════════════════════════════
## QUICKSTART

**1 pages in this section:**

### Warp quickstart
**Path:** `/quickstart`
**Summary:** Get up and running with Warp in about 10 minutes. Install, run your first commands, talk to an agent, and discover what makes Warp different.


════════════════════════════════════════════════════════════════════════════════
## REFERENCE

**33 pages in this section:**

### Technical reference
**Path:** `/reference`
**Summary:** Technical reference documentation for the Oz CLI, API, and SDK.

### Oz API & SDK reference
**Path:** `/reference/api-and-sdk`
**Summary:** Create and inspect cloud agent runs over HTTP with the Oz API, or use the Python and TypeScript SDKs for typed requests, retries, and error handling.

### Demo: Sentry monitoring with SDK
**Path:** `/reference/api-and-sdk/demo-sentry-monitoring-with-sdk`
**Summary:** Build a Sentry webhook handler that triggers agents to investigate errors and create draft PRs.

### API & SDK quickstart
**Path:** `/reference/api-and-sdk/quickstart`
**Summary:** Create and monitor your first cloud agent run via the Oz API or SDK in ~5 minutes.

### API Troubleshooting
**Path:** `/reference/api-and-sdk/troubleshooting`
**Summary:** Troubleshooting resources for the Oz API and SDK, including a full reference for all platform error codes.

### Errors Overview
**Path:** `/reference/api-and-sdk/troubleshooting/errors`
**Summary:** Reference for all error codes returned by the Oz platform API. Each error includes an HTTP status, machine-readable code, and actionable resolution steps.

### authentication_required
**Path:** `/reference/api-and-sdk/troubleshooting/errors/authentication-required`
**Summary:** The API key in the request is invalid, expired, or missing. Generate a new key and update your client configuration.

### budget_exceeded
**Path:** `/reference/api-and-sdk/troubleshooting/errors/budget-exceeded`
**Summary:** Your team's configured spending budget limit has been reached. Increase the budget or wait for the budget period to reset.

### Error: conflict (409)
**Path:** `/reference/api-and-sdk/troubleshooting/errors/conflict`
**Summary:** The request conflicts with the current state of the resource. Wait for the resource to reach the expected state and retry.

### content_policy_violation
**Path:** `/reference/api-and-sdk/troubleshooting/errors/content-policy-violation`
**Summary:** The task prompt or environment setup commands were flagged by the platform's automated content policy checks.

### environment_setup_failed
**Path:** `/reference/api-and-sdk/troubleshooting/errors/environment-setup-failed`
**Summary:** The cloud agent's environment failed to initialize. Check repo URLs, setup commands, and working directory paths.

### external_authentication_required
**Path:** `/reference/api-and-sdk/troubleshooting/errors/external-authentication-required`
**Summary:** The task requires access to an external service (GitHub, Slack, Linear, etc.) that hasn't been authorized. Follow the auth_url to grant access.

### feature_not_available
**Path:** `/reference/api-and-sdk/troubleshooting/errors/feature-not-available`
**Summary:** The requested feature is not included in your current plan. Upgrade your team's plan to access this capability.

### insufficient_credits
**Path:** `/reference/api-and-sdk/troubleshooting/errors/insufficient-credits`
**Summary:** Your team has exhausted all Add-on Credits for cloud agent usage. Purchase more credits from your team's billing settings to continue.

### integration_disabled
**Path:** `/reference/api-and-sdk/troubleshooting/errors/integration-disabled`
**Summary:** The integration (Slack, Linear, etc.) is currently disabled in the Oz settings. Enable it to continue.

### integration_not_configured
**Path:** `/reference/api-and-sdk/troubleshooting/errors/integration-not-configured`
**Summary:** The integration's setup is incomplete. Visit the setup URL to finish configuring the integration.

### internal_error
**Path:** `/reference/api-and-sdk/troubleshooting/errors/internal-error`
**Summary:** An unexpected server-side error occurred. The platform will automatically retry. Contact support if the issue persists.

### invalid_request
**Path:** `/reference/api-and-sdk/troubleshooting/errors/invalid-request`
**Summary:** The request body is malformed, missing required fields, or contains invalid parameter values.

### not_authorized
**Path:** `/reference/api-and-sdk/troubleshooting/errors/not-authorized`
**Summary:** The authenticated user or API key does not have permission to perform the requested operation.

### operation_not_supported
**Path:** `/reference/api-and-sdk/troubleshooting/errors/operation-not-supported`
**Summary:** The requested operation is not supported for this resource or its current state.

### resource_not_found
**Path:** `/reference/api-and-sdk/troubleshooting/errors/resource-not-found`
**Summary:** The requested resource (task, environment, schedule, agent, etc.) does not exist or has been deleted.

### resource_unavailable
**Path:** `/reference/api-and-sdk/troubleshooting/errors/resource-unavailable`
**Summary:** A transient infrastructure issue prevented the task from running. The platform will automatically retry. No action is needed.

### Oz CLI reference
**Path:** `/reference/cli`
**Summary:** Use the Oz CLI to run, configure, and manage agents from the terminal.

### Agent profiles
**Path:** `/reference/cli/agent-profiles`
**Summary:** Use agent profiles with the Oz CLI to control what the agent can access, how it behaves, and where it can act.

### API keys for the Oz CLI
**Path:** `/reference/cli/api-keys`
**Summary:** Create and manage API keys for authenticating the Oz CLI and cloud agents.

### Artifacts
**Path:** `/reference/cli/artifacts`
**Summary:** Get metadata for and download files produced by an agent run using the `oz artifact` subcommands.

### Federated identity tokens
**Path:** `/reference/cli/federate`
**Summary:** Issue short-lived OIDC identity tokens from a running agent so it can authenticate to cloud providers without long-lived credentials.

### Integration setup
**Path:** `/reference/cli/integration-setup`
**Summary:** Learn how to set up environments and integrations so you can trigger Oz agents from external tools.

### MCP servers (CLI reference)
**Path:** `/reference/cli/mcp-servers`
**Summary:** Connect agents to external tools like GitHub, Linear, and Sentry by passing MCP servers to the --mcp flag as a UUID, inline JSON, or file path.

### CLI quickstart
**Path:** `/reference/cli/quickstart`
**Summary:** Set up and run your first cloud agent via the Oz CLI in less than 5 minutes.

### Skills via the Oz CLI
**Path:** `/reference/cli/skills`
**Summary:** Use skills with the Oz CLI to run agents from reusable skill definitions stored in your repositories.

### CLI Troubleshooting
**Path:** `/reference/cli/troubleshooting`
**Summary:** Solutions for common Oz CLI errors — including authentication issues, agent failures, environments, GitHub access, and Docker image issues.

### Warp Drive context
**Path:** `/reference/cli/warp-drive`
**Summary:** Use saved prompts, notebooks, workflows, and rules from Warp Drive as context in CLI agent commands.


════════════════════════════════════════════════════════════════════════════════
## SUPPORT-AND-COMMUNITY

**23 pages in this section:**

### Support & Community
**Path:** `/support-and-community`
**Summary:** Connect with the developers and engineers building with Warp. Share what you've built, shape what we build next, and get help when you're stuck.

### Contributing to Warp
**Path:** `/support-and-community/community/contributing`
**Summary:** Contribute to Warp's open source client by filing issues, opening pull requests, building themes, and sharing workflows.

### Open Source Licenses
**Path:** `/support-and-community/community/open-source-licenses`
**Summary:** These are the third-party libraries that Warp depends on.

### Oz Open Source Partnership
**Path:** `/support-and-community/community/open-source-partnership`
**Summary:** Warp supports high-impact open source projects with free agent credits through the Oz Open Source Partnership program.

### Refer a friend and earn rewards
**Path:** `/support-and-community/community/refer-a-friend`
**Summary:** Think Warp would be the ideal product for someone you know? You can invite your team or friends within the app and earn rewards.

### Warp Preview program
**Path:** `/support-and-community/community/warp-preview-and-alpha-program`
**Summary:** Warp Preview is an early-access build of Warp with experimental features. Try what's next before it ships.

### Plans and billing
**Path:** `/support-and-community/plans-and-billing`
**Summary:** Understand your Warp plan options, how credits work, and how to manage billing settings.

### Add-on Credits
**Path:** `/support-and-community/plans-and-billing/add-on-credits`
**Summary:** Purchase Add-on Credits to keep using premium AI models after reaching your monthly credit limit.

### Bring Your Own API Key
**Path:** `/support-and-community/plans-and-billing/bring-your-own-api-key`
**Summary:** Warp's paid plans include the ability to bring your own API keys (BYOK) for OpenAI, Anthropic, and Google AI models.

### Warp credits and billing
**Path:** `/support-and-community/plans-and-billing/credits`
**Summary:** Details on Warp credits and how they are calculated.

### Overages (Legacy)
**Path:** `/support-and-community/plans-and-billing/overages-legacy`
**Summary:** Pay-as-you-go access to premium AI models after reaching your monthly credits quota on Warps plans.

### Plans, pricing, and refunds
**Path:** `/support-and-community/plans-and-billing/plans-pricing-refunds`
**Summary:** Learn about Warp's plans and pricing tiers. Get started for free.

### Platform credits
**Path:** `/support-and-community/plans-and-billing/platform-credits`
**Summary:** Platform credits cover Warp's platform layer on every cloud agent run and on local runs with customer-supplied inference. Learn when they apply.

### Pricing and billing FAQs
**Path:** `/support-and-community/plans-and-billing/pricing-faqs`
**Summary:** Frequently asked questions about upgrading, managing billing, refunds, and invoicing with Warp's paid plans.

### Warp network log
**Path:** `/support-and-community/privacy-and-security/network-log`
**Summary:** Logs for all network traffic (both requests and responses) originating from the current terminal session.

### Privacy and data control
**Path:** `/support-and-community/privacy-and-security/privacy`
**Summary:** Warp's approach to privacy and your control over your data

### Secret Redaction
**Path:** `/support-and-community/privacy-and-security/secret-redaction`
**Summary:** Secret Redaction detects and redacts secrets, passwords, API keys, and PII in your terminal output before sending data to servers.

### Known issues and workarounds
**Path:** `/support-and-community/troubleshooting-and-support/known-issues`
**Summary:** Known Warp issues with workarounds, including SSH, shells, and incompatible tools.

### Logging out & uninstalling
**Path:** `/support-and-community/troubleshooting-and-support/logging-out-and-uninstalling`
**Summary:** How to log out from Warp, and how to uninstall Warp.

### Sending feedback and logs
**Path:** `/support-and-community/troubleshooting-and-support/sending-us-feedback`
**Summary:** Send Warp feedback, bug reports, and feature requests, and gather logs, crash reports, CPU samples, and AI conversation IDs to attach to them.

### Troubleshooting Login
**Path:** `/support-and-community/troubleshooting-and-support/troubleshooting-login-issues`
**Summary:** Fix common login issues including SSO, proxies, ad blockers, and auth tokens.

### Updating Warp
**Path:** `/support-and-community/troubleshooting-and-support/updating-warp`
**Summary:** Check for updates, troubleshoot auto-update permissions, and refresh signing keys.

### Using Warp Offline
**Path:** `/support-and-community/troubleshooting-and-support/using-warp-offline`
**Summary:** Using Warp offline and what features are supported.


════════════════════════════════════════════════════════════════════════════════
## TERMINAL
*Terminal features: blocks, input, output, tabs, themes, and more*

**71 pages in this section:**

### Terminal appearance overview
**Path:** `/terminal/appearance`
**Summary:** Customize Warp's visual appearance, including themes, fonts, prompts, app icons, input position, and pane behavior.

### Custom app icons
**Path:** `/terminal/appearance/app-icons`
**Summary:** Choose from a palette of built-in app icons to customize Warp's dock appearance on macOS.

### Blocks Behavior
**Path:** `/terminal/appearance/blocks-behavior`
**Summary:** Customize Block spacing with Compact mode and toggle Block dividers for a cleaner layout.

### Custom Themes
**Path:** `/terminal/appearance/custom-themes`
**Summary:** Warp supports Custom Themes which can be created manually or downloaded from our repo.

### Input position
**Path:** `/terminal/appearance/input-position`
**Summary:** Warp gives you the ability to configure the position of your input, which includes both the prompt and the command line.

### Pane Dimming & Focus
**Path:** `/terminal/appearance/pane-dimming`
**Summary:** Warp supports dimming inactive Panes as well as allowing the focus to follow the mouse. This helps you easily see which pane is active and maintain focus.

### Terminal prompt
**Path:** `/terminal/appearance/prompt`
**Summary:** Configure Warp's native prompt with context chips or use your own Shell prompt (PS1).

### Size, Opacity, & Blurring
**Path:** `/terminal/appearance/size-opacity-blurring`
**Summary:** Configure window size, opacity, and background blurring to match your visual preferences.

### Tabs Behavior
**Path:** `/terminal/appearance/tabs-behavior`
**Summary:** Customize tab behavior in Warp, including tab indicators, tab bar visibility, and close button position.

### Text, Fonts, & Cursor
**Path:** `/terminal/appearance/text-fonts-cursor`
**Summary:** Warp supports customizing the font and how text is displayed. This can help improve readability and usability. Warp also supports disabling the blinking cursor.

### Terminal themes
**Path:** `/terminal/appearance/themes`
**Summary:** Warp includes several themes (out-of-box) and also supports setting custom themes.

### Terminal Blocks overview
**Path:** `/terminal/blocks`
**Summary:** A Block groups commands and outputs into one atomic unit.

### Background Blocks
**Path:** `/terminal/blocks/background-blocks`
**Summary:** How Blocks interact with background process output.

### Block Actions
**Path:** `/terminal/blocks/block-actions`
**Summary:** Copy, bookmark, share, search, and filter Blocks using built-in actions.

### Terminal Block Basics
**Path:** `/terminal/blocks/block-basics`
**Summary:** The basics of creating, selecting, and navigating between Blocks.

### Block Filtering
**Path:** `/terminal/blocks/block-filtering`
**Summary:** Filter Block output by text, regex, or case to focus on specific matching lines.

### Block Sharing
**Path:** `/terminal/blocks/block-sharing`
**Summary:** Share Blocks with your team as permalinks or embeddable HTML snippets.

### Terminal Block Find
**Path:** `/terminal/blocks/find`
**Summary:** Search across Blocks from the bottom up, with regex, case-sensitive, and per-Block filtering options.

### Sticky Command Header
**Path:** `/terminal/blocks/sticky-command-header`
**Summary:** Pin the running command at the top of the screen when scrolling through large Block outputs.

### Command completions overview
**Path:** `/terminal/command-completions`
**Summary:** Warp's main features for command completions and autosuggestions.

### Autosuggestions
**Path:** `/terminal/command-completions/autosuggestions`
**Summary:** Warp will automatically suggest commands as you type based on shell history and possible completions.

### Tab completions
**Path:** `/terminal/command-completions/completions`
**Summary:** Get fuzzy-matched suggestions for commands, options, and paths by pressing Tab anywhere.

### Command Palette
**Path:** `/terminal/command-palette`
**Summary:** Command Palette is a global search to quickly locate Workflows, Notebooks, keyboard shortcuts, or other actions within Warp.

### Terminal comparisons overview
**Path:** `/terminal/comparisons`
**Summary:** Compare Warp's performance and terminal feature support against other popular terminal emulators like iTerm2, Alacritty, and WezTerm.

### Performance benchmarks
**Path:** `/terminal/comparisons/performance`
**Summary:** This is a short comparison of different terminals and their performance.

### Terminal features
**Path:** `/terminal/comparisons/terminal-features`
**Summary:** Below you'll find a table showcasing different terminal features (such as text attribution) and information about which one of those are supported in Warp.

### Modern text editing overview
**Path:** `/terminal/editor`
**Summary:** Unlike other terminals, Warp’s input editor operates out of the box like a modern IDE and the text editors we’re used to.

### Alias Expansion
**Path:** `/terminal/editor/alias-expansion`
**Summary:** Warp will automatically expand your aliases as you type in the input editor.

### Command Inspector
**Path:** `/terminal/editor/command-inspector`
**Summary:** Command Inspector (also known as Command X-Ray) surfaces documentation for sub-parts of your command, directly in Warp's Input Editor.

### Syntax & Error Highlighting
**Path:** `/terminal/editor/syntax-error-highlighting`
**Summary:** Color-code commands and underline errors in real time as you type in Warp's input editor.

### Input editor Vim keybindings
**Path:** `/terminal/editor/vim`
**Summary:** Use input editor Vim keybindings (also known as Vim mode) to edit commands quickly in Warp.

### Command entry overview
**Path:** `/terminal/entry`
**Summary:** Warp's main features for Command Entry, History, Synchronized Inputs, YAML Workflows and More!

### Command Corrections
**Path:** `/terminal/entry/command-corrections`
**Summary:** Command Corrections provides auto-correct suggestions on previously run commands to catch typos and forgotten flags, and fix general console errors.

### Command History
**Path:** `/terminal/entry/command-history`
**Summary:** Command History helps you quickly find previously run commands.

### Command Search
**Path:** `/terminal/entry/command-search`
**Summary:** Search command history, Workflows, Prompts, and agent conversations with fuzzy matching.

### Synchronized Inputs
**Path:** `/terminal/entry/synchronized-inputs`
**Summary:** Type a command once and sync it to multiple panes simultaneously.

### YAML Workflows
**Path:** `/terminal/entry/yaml-workflows`
**Summary:** Workflows are an easier way to execute and share commands within Warp.

### Classic Input
**Path:** `/terminal/input/classic-input`
**Summary:** Classic Input lets you use Warp with an editor that resembles a traditional terminal, offering full terminal features and Agent Mode support out of the box.

### Universal Input (Legacy)
**Path:** `/terminal/input/universal-input`
**Summary:** Universal Input was the previous default input interface for Warp, replaced by Terminal and Agent modes.

### Terminal Integrations
**Path:** `/terminal/integrations-and-plugins`
**Summary:** Warp's terminal functionality extends and integrates with popular development tools.

### More features overview
**Path:** `/terminal/more-features`
**Summary:** Explore additional Warp terminal features beyond the essentials.

### Accessibility
**Path:** `/terminal/more-features/accessibility`
**Summary:** Warp's accessibility features include VoiceOver support, voice input, and configurable verbosity.

### Audible terminal bell
**Path:** `/terminal/more-features/audible-bell`
**Summary:** Enable an audible terminal bell in Warp that can be triggered by CLI tools like ping.

### Files, Links, & Scripts
**Path:** `/terminal/more-features/files-and-links`
**Summary:** Quickly open links and files or run scripts with your mouse.

### Full-screen apps
**Path:** `/terminal/more-features/full-screen-apps`
**Summary:** Run Vim, Emacs, and other full-screen apps with configurable mouse reporting and padding.

### Warp for Linux
**Path:** `/terminal/more-features/linux`
**Summary:** Linux-specific features including native Wayland support and crash recovery.

### Markdown Viewer
**Path:** `/terminal/more-features/markdown-viewer`
**Summary:** Open Markdown files in your terminal and run commands.

### Desktop Notifications
**Path:** `/terminal/more-features/notifications`
**Summary:** Receive desktop notifications when long-running commands complete or need your input.

### Terminal quit warning
**Path:** `/terminal/more-features/quit-warning`
**Summary:** Warp's quit warning feature is a valuable precaution to prevent unintentional data loss or lost progress on long-running jobs.

### Settings Sync
**Path:** `/terminal/more-features/settings-sync`
**Summary:** Keep your Warp settings consistent across devices and sessions with cloud-based sync.

### Text selection
**Path:** `/terminal/more-features/text-selection`
**Summary:** Use smart selection and rectangular (column) selection to quickly highlight text in Warp.

### Warp URI Scheme
**Path:** `/terminal/more-features/uri-scheme`
**Summary:** Warps URI scheme enables you to programmatically open new windows, tabs, or launch configurations with ease.

### Working Directory
**Path:** `/terminal/more-features/working-directory`
**Summary:** Set a default working directory for new Warp sessions, with options for home directory, previous session, custom path, or per-window/tab/pane configuration.

### Sessions overview
**Path:** `/terminal/sessions`
**Summary:** Navigate between sessions and automatically restore windows, tabs, and panes when you relaunch Warp.

### Launch Configurations (Legacy)
**Path:** `/terminal/sessions/launch-configurations`
**Summary:** Launch Configurations (Legacy) let you save a configuration of windows, tabs, and panes. For new setups, use Tab Configs instead.

### Session Navigation
**Path:** `/terminal/sessions/session-navigation`
**Summary:** Quickly navigate to any terminal session across Warp using the Session Navigation palette.

### Session Restoration
**Path:** `/terminal/sessions/session-restoration`
**Summary:** Restore your windows, tabs, panes, and recent Blocks automatically when you relaunch Warp.

### Settings file
**Path:** `/terminal/settings`
**Summary:** Configure Warp with a plain-text TOML settings file. Learn where it lives, how it works with the Settings panel, and see common configuration examples.

### All settings reference
**Path:** `/terminal/settings/all-settings`
**Summary:** Complete reference for every setting available in Warp's settings.toml file, organized by section with descriptions, types, defaults, and examples.

### File and folder locations
**Path:** `/terminal/settings/file-locations`
**Summary:** Reference for where Warp stores config, themes, tab configs, settings, keybindings, logs, and other files on macOS, Windows, and Linux.

### Warpify overview
**Path:** `/terminal/warpify`
**Summary:** Warp support for Warpifying, or enabling Warp's features, in local or remote sessions.

### SSH with Warp features
**Path:** `/terminal/warpify/ssh`
**Summary:** Use Warp's SSH extension on remote macOS and Linux hosts to get a real file tree, reliable completions, and native code edits over SSH.

### Legacy SSH wrapper
**Path:** `/terminal/warpify/ssh-legacy`
**Summary:** Legacy SSH wrapper that bootstraps Warp features on remote machines without tmux.

### Warpify subshells
**Path:** `/terminal/warpify/subshells`
**Summary:** Warpify subshells in bash, zsh, and fish to get Warp features in nested sessions.

### Windows and tabs overview
**Path:** `/terminal/windows`
**Summary:** Manage Warp windows, tabs, vertical tabs, split panes, and tab configurations with global hotkeys and reusable layouts.

### Configurable toolbar
**Path:** `/terminal/windows/configurable-toolbar`
**Summary:** Reorder, hide, and move panel toggle buttons between the left and right sides of Warp's header toolbar to match your workflow.

### Global Hotkey
**Path:** `/terminal/windows/global-hotkey`
**Summary:** Show or hide Warp instantly with a global hotkey, including a dedicated Quake-style drop-down window.

### Split panes
**Path:** `/terminal/windows/split-panes`
**Summary:** The split panes feature allows you to divide a tab into multiple rectangular panes, each of which is a unique terminal session.

### Tab Configs
**Path:** `/terminal/windows/tab-configs`
**Summary:** Tab Configs let you define reusable tab setups — including directory, startup commands, pane layout, shell, and theme — in a simple TOML file.

### Tabs
**Path:** `/terminal/windows/tabs`
**Summary:** Organize your window into multiple terminal sessions with customizable tabs, complete with titles and ANSI colors.

### Vertical Tabs
**Path:** `/terminal/windows/vertical-tabs`
**Summary:** The vertical tabs panel replaces the horizontal tab bar with a sidebar showing rich metadata, drag-and-drop management, and display options for tabs and panes.


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
