# nanobot documentation knowledge map

Discovered Markdown files (in scope):
- [`README.md`](../README.md)
- [`SECURITY.md`](../SECURITY.md)
- [`COMMUNICATION.md`](../COMMUNICATION.md)
- [`workspace/AGENTS.md`](../workspace/AGENTS.md)
- [`workspace/TOOLS.md`](../workspace/TOOLS.md)
- [`workspace/HEARTBEAT.md`](../workspace/HEARTBEAT.md)
- [`workspace/SOUL.md`](../workspace/SOUL.md)
- [`workspace/USER.md`](../workspace/USER.md)
- [`workspace/memory/MEMORY.md`](../workspace/memory/MEMORY.md)
- [`nanobot/skills/README.md`](../nanobot/skills/README.md)
- [`nanobot/skills/github/SKILL.md`](../nanobot/skills/github/SKILL.md)
- [`nanobot/skills/weather/SKILL.md`](../nanobot/skills/weather/SKILL.md)
- [`nanobot/skills/summarize/SKILL.md`](../nanobot/skills/summarize/SKILL.md)
- [`nanobot/skills/tmux/SKILL.md`](../nanobot/skills/tmux/SKILL.md)
- [`nanobot/skills/cron/SKILL.md`](../nanobot/skills/cron/SKILL.md)
- [`nanobot/skills/skill-creator/SKILL.md`](../nanobot/skills/skill-creator/SKILL.md)

## 1) Repository at-a-glance

**nanobot** is an ultra-lightweight personal AI assistant (Python) that provides “core agent functionality” in a small codebase, including a CLI, tool execution, configurable LLM providers, optional local-model support (vLLM), and chat app “channels” like Telegram/Discord/WhatsApp/Feishu. (source: README.md)

**Who it’s for (as documented)**:
- **Users**: People who want a working personal assistant quickly (CLI quickstart + config in `~/.nanobot/config.json`). (source: README.md#quick-start)
- **Researchers / hackers**: The repo emphasizes readability, small size, and “research-ready” iteration. (source: README.md#key-features-of-nanobot)
- **Operators (lightweight)**: There is explicit “production deployment” security guidance and Docker instructions. (source: SECURITY.md#7-production-deployment, README.md#-docker)

**Primary newcomer entry points**:
- [`README.md`](../README.md): install, quick start, configuration, channels, Docker, project structure. (source: README.md)
- [`SECURITY.md`](../SECURITY.md): best practices + production hardening checklist. (source: SECURITY.md)
- [`workspace/` templates](../workspace/): how the agent workspace is structured (tools, memory, heartbeat). (source: workspace/AGENTS.md, workspace/TOOLS.md, workspace/HEARTBEAT.md)
- [`nanobot/skills/`](../nanobot/skills/): what “skills” are and what built-ins exist. (source: nanobot/skills/README.md)

## 2) Documentation inventory (table)

One row per Markdown file; links are relative to `knowledge/overview.md`.

| Path | Title | Purpose | Key topics | Dependencies / references to other docs | Confidence |
|---|---|---|---|---|---|
| [`README.md`](../README.md) | nanobot: Ultra-Lightweight Personal AI Assistant | Primary user-facing entry point: what nanobot is + install/run/configure + major features. (source: README.md) | - Install (source/PyPI/uv)<br>- Quick start (`nanobot onboard`, config, `nanobot agent`)<br>- Local models via vLLM<br>- Chat “channels” (Telegram/Discord/WhatsApp/Feishu)<br>- Security knobs (`allowFrom`, `restrictToWorkspace`)<br>- CLI command list<br>- Docker usage<br>- Repo structure outline (source: README.md) | Links to `COMMUNICATION.md` for community groups. (source: README.md)<br>Mentions `~/.nanobot/config.json` and security settings also described in `SECURITY.md`. (source: README.md#configuration, SECURITY.md) | High |
| [`SECURITY.md`](../SECURITY.md) | Security Policy | Security reporting + operational hardening guidance for running nanobot safely. (source: SECURITY.md) | - Vulnerability reporting process<br>- API key management + file permissions (`chmod 600`)<br>- Channel allow-lists (`allowFrom`)<br>- Shell/file/network risk notes<br>- Dependency security (`pip-audit`, `npm audit`)<br>- Production isolation + non-root guidance<br>- Incident response checklist + limitations (source: SECURITY.md) | References “Release Notes” and GitHub security advisories; complements README’s config/security section. (source: SECURITY.md#updates, README.md#security) | High |
| [`COMMUNICATION.md`](../COMMUNICATION.md) | Inference: Communication / discussion groups | QR codes for joining HKUDS discussion groups (WeChat/Feishu). (source: COMMUNICATION.md) | - WeChat group access via QR<br>- Feishu group access via QR (source: COMMUNICATION.md) | Linked from `README.md`. (source: README.md) | Med |
| [`workspace/AGENTS.md`](../workspace/AGENTS.md) | Agent Instructions | Template guidance for how an agent should behave inside the “workspace” context. (source: workspace/AGENTS.md) | - Interaction guidelines (concise, clarify ambiguity)<br>- Tool categories (file ops, shell, web, messaging, spawn)<br>- Memory file conventions (`memory/`, `MEMORY.md`)<br>- Scheduled reminders via `nanobot cron add ...`<br>- Heartbeat task file (`HEARTBEAT.md`) semantics (source: workspace/AGENTS.md) | Mentions `memory/` and `MEMORY.md`, plus `HEARTBEAT.md` and `nanobot cron` usage that also appears in `README.md`. (source: workspace/AGENTS.md, workspace/memory/MEMORY.md, workspace/HEARTBEAT.md, README.md#cli-reference) | Med |
| [`workspace/TOOLS.md`](../workspace/TOOLS.md) | Available Tools | Defines the tool surface area conceptually (names, signatures, safety notes) in the workspace docs. (source: workspace/TOOLS.md) | - File ops: `read_file`, `write_file`, `edit_file`, `list_dir`<br>- Shell: `exec` + safety notes/timeout/truncation<br>- Web: `web_search`, `web_fetch` + config requirement<br>- Messaging: `message`<br>- Background tasks: `spawn`<br>- Heartbeat task management patterns<br>- “Adding Custom Tools” pointers (source: workspace/TOOLS.md) | References `HEARTBEAT.md` and tool-based scheduling patterns; references code locations for adding tools (`nanobot/agent/tools/`, `AgentLoop._register_default_tools()`). (source: workspace/TOOLS.md) | High |
| [`workspace/HEARTBEAT.md`](../workspace/HEARTBEAT.md) | Heartbeat Tasks | Template file describing periodic “heartbeat” tasks checked every 30 minutes. (source: workspace/HEARTBEAT.md) | - Heartbeat concept (“checked every 30 minutes”)<br>- Where to add tasks (“Active Tasks” section)<br>- Completed task handling (source: workspace/HEARTBEAT.md) | Referenced by `workspace/AGENTS.md` and `workspace/TOOLS.md`. (source: workspace/AGENTS.md, workspace/TOOLS.md) | Med |
| [`workspace/SOUL.md`](../workspace/SOUL.md) | Soul | Template describing nanobot’s personality, values, and communication style. (source: workspace/SOUL.md) | - Identity (“I am nanobot”)<br>- Personality traits<br>- Values (accuracy, privacy/safety, transparency)<br>- Communication guidelines (source: workspace/SOUL.md) | No explicit references found. (source: workspace/SOUL.md) | Med |
| [`workspace/USER.md`](../workspace/USER.md) | User Profile | Blank-ish template for user personalization fields (name/timezone/style/role/etc.). (source: workspace/USER.md) | - User metadata fields<br>- Communication style prefs checklist<br>- Response length prefs checklist<br>- Technical level prefs checklist<br>- Work context placeholders (source: workspace/USER.md) | No explicit references found. (source: workspace/USER.md) | Low |
| [`workspace/memory/MEMORY.md`](../workspace/memory/MEMORY.md) | Long-term Memory | Template file for persistent memory across sessions (user info, preferences, project context). (source: workspace/memory/MEMORY.md) | - What “long-term memory” stores<br>- Suggested buckets: user info / preferences / project context / notes<br>- “Automatically updated” note (source: workspace/memory/MEMORY.md) | Mentioned by `workspace/AGENTS.md`. (source: workspace/AGENTS.md) | Low |
| [`nanobot/skills/README.md`](../nanobot/skills/README.md) | nanobot Skills | Explains the built-in “skills” directory, the `SKILL.md` format, and lists available skills. (source: nanobot/skills/README.md) | - Skill format (`SKILL.md` per skill directory)<br>- YAML frontmatter expectation<br>- Attribution to OpenClaw skill system<br>- Built-in skills list (github/weather/summarize/tmux/skill-creator) (source: nanobot/skills/README.md) | Points to the individual skill docs; conceptually complements README’s “Project Structure” mention of `skills/`. (source: nanobot/skills/README.md, README.md#-project-structure) | High |
| [`nanobot/skills/github/SKILL.md`](../nanobot/skills/github/SKILL.md) | GitHub Skill | Procedure for using GitHub CLI (`gh`) for PR/issues/CI/API queries. (source: nanobot/skills/github/SKILL.md) | - `gh pr checks` usage<br>- `gh run list/view` usage<br>- `gh api` for advanced queries<br>- `--json` + `--jq` filtering patterns (source: nanobot/skills/github/SKILL.md) | Depends on `gh` binary presence (declared in metadata); no direct cross-doc links. (source: nanobot/skills/github/SKILL.md) | High |
| [`nanobot/skills/weather/SKILL.md`](../nanobot/skills/weather/SKILL.md) | Weather | How to fetch weather via `wttr.in` (primary) or Open-Meteo JSON (fallback) using `curl`. (source: nanobot/skills/weather/SKILL.md) | - `wttr.in` formats + tips (units, airport codes, today-only)<br>- Open-Meteo JSON query pattern<br>- No API keys required (source: nanobot/skills/weather/SKILL.md) | Depends on `curl` binary (declared in metadata); external service docs linked. (source: nanobot/skills/weather/SKILL.md) | High |
| [`nanobot/skills/summarize/SKILL.md`](../nanobot/skills/summarize/SKILL.md) | Summarize | How to use the `summarize` CLI to summarize URLs/files/YouTube; includes env-var key mapping. (source: nanobot/skills/summarize/SKILL.md) | - Trigger phrases (“summarize this URL”, etc.)<br>- CLI quickstart examples<br>- Transcript extraction best-effort flow<br>- Provider API key env vars<br>- Config file location (`~/.summarize/config.json`)<br>- Useful flags (length/json/extract-only) (source: nanobot/skills/summarize/SKILL.md) | Depends on `summarize` binary and optional `FIRECRAWL_API_KEY` / `APIFY_API_TOKEN`. (source: nanobot/skills/summarize/SKILL.md) | High |
| [`nanobot/skills/tmux/SKILL.md`](../nanobot/skills/tmux/SKILL.md) | tmux Skill | How to use tmux for interactive TTY workflows, socket conventions, monitoring output, and orchestration tips. (source: nanobot/skills/tmux/SKILL.md) | - When to use tmux vs non-interactive exec<br>- Private socket conventions (`NANOBOT_TMUX_SOCKET_DIR`)<br>- Capturing output + waiting for prompts<br>- Safe send-keys patterns<br>- Cleanup patterns<br>- References to helper scripts (source: nanobot/skills/tmux/SKILL.md) | References bundled scripts `scripts/find-sessions.sh` and `scripts/wait-for-text.sh` in the same skill folder. (source: nanobot/skills/tmux/SKILL.md) | High |
| [`nanobot/skills/cron/SKILL.md`](../nanobot/skills/cron/SKILL.md) | Cron | Describes scheduling reminders/tasks using a `cron` tool abstraction and mapping user phrasing to parameters. (source: nanobot/skills/cron/SKILL.md) | - Reminder vs task modes (conceptual)<br>- Add/list/remove examples (tool-call style)<br>- “Time expressions” mapping table (source: nanobot/skills/cron/SKILL.md) | Overlaps with README’s CLI cron commands (`nanobot cron ...`) and workspace instructions. (source: README.md#cli-reference, workspace/AGENTS.md) | Med |
| [`nanobot/skills/skill-creator/SKILL.md`](../nanobot/skills/skill-creator/SKILL.md) | Skill Creator | Comprehensive guidance for designing and packaging “skills” (format, principles, progressive disclosure, packaging scripts). (source: nanobot/skills/skill-creator/SKILL.md) | - What skills are and what they provide<br>- Context-budget principles (“concise is key”)<br>- Skill anatomy (`SKILL.md`, scripts/references/assets)<br>- Progressive disclosure patterns<br>- Naming rules<br>- Initialization/packaging scripts and workflow (source: nanobot/skills/skill-creator/SKILL.md) | Refers to scripts like `scripts/init_skill.py` and `scripts/package_skill.py` (not documented elsewhere in Markdown in this repo). (source: nanobot/skills/skill-creator/SKILL.md) | Med |

## 3) Knowledge structure (map)

Below is a mental model of the repo’s documented knowledge domains and where each domain lives.

### Product_overview_and_getting_started

What you’ll learn here: what nanobot is, how to install it, how to get to “first successful chat,” and what major capabilities are supported. (source: README.md)

- [`README.md`](../README.md)

### Configuration_and_security_controls

What you’ll learn here: how nanobot is configured (notably `~/.nanobot/config.json`) and what security controls/operational practices the docs recommend for safer usage (permissions, allow-lists, non-root, isolation, dependency updates). (source: README.md#configuration, SECURITY.md)

- [`README.md`](../README.md) (configuration + security options) (source: README.md#configuration)
- [`SECURITY.md`](../SECURITY.md) (hardening + incident response) (source: SECURITY.md)

### Channels_and_chat_apps

What you’ll learn here: how to run nanobot as a “gateway” connected to messaging platforms, what credentials are needed, and the configuration shape for each supported channel. (source: README.md#-chat-apps)

- [`README.md`](../README.md) (Telegram/Discord/WhatsApp/Feishu sections) (source: README.md#-chat-apps)
- [`COMMUNICATION.md`](../COMMUNICATION.md) (community groups) (source: COMMUNICATION.md)

### Providers_and_models

What you’ll learn here: how providers are described (OpenRouter, Anthropic, OpenAI, DeepSeek, Groq, Gemini, Moonshot/Kimi, vLLM) and how local-model usage via vLLM is configured. (source: README.md#-local-models-vllm, README.md#providers)

- [`README.md`](../README.md) (providers table + vLLM instructions) (source: README.md#providers)
- [`knowledge/setup-agent.md`](setup-agent.md) — Agent setup: config location, `agents.defaults`, provider selection, and examples (Moonshot, Anthropic, OpenRouter, etc.).
- [`knowledge/ai-model-setup.md`](ai-model-setup.md) — How nanobot chooses the LLM provider, LiteLLM conventions, and detailed provider notes.

### Runtime_and_operations

What you’ll learn here: what CLI commands exist (agent/gateway/status/channels/cron), how Docker usage is documented, and how the docs recommend deploying/operating nanobot more safely in production-like contexts. (source: README.md#cli-reference, README.md#-docker, SECURITY.md#7-production-deployment)

- [`README.md`](../README.md) (CLI + Docker) (source: README.md#cli-reference)
- [`SECURITY.md`](../SECURITY.md) (production isolation, logging, incident response) (source: SECURITY.md#7-production-deployment)

### Workspace_templates_memory_and_heartbeat

What you’ll learn here: the repo’s documented “workspace” file conventions (agent instructions, tool list, heartbeat periodic tasks, memory files, and user profile/personality templates). (source: workspace/AGENTS.md, workspace/TOOLS.md, workspace/HEARTBEAT.md, workspace/memory/MEMORY.md)

- [`workspace/AGENTS.md`](../workspace/AGENTS.md) (agent behavior + reminders/heartbeat notes) (source: workspace/AGENTS.md)
- [`workspace/TOOLS.md`](../workspace/TOOLS.md) (tool descriptions + custom tool pointers) (source: workspace/TOOLS.md)
- [`workspace/HEARTBEAT.md`](../workspace/HEARTBEAT.md) (heartbeat task file semantics) (source: workspace/HEARTBEAT.md)
- [`workspace/memory/MEMORY.md`](../workspace/memory/MEMORY.md) (long-term memory template) (source: workspace/memory/MEMORY.md)
- [`workspace/USER.md`](../workspace/USER.md) and [`workspace/SOUL.md`](../workspace/SOUL.md) (personalization templates) (source: workspace/USER.md, workspace/SOUL.md)

### Skills_system_and_skill_library

What you’ll learn here: what a “skill” is in this repo’s terminology, what built-ins exist, and how specific skills instruct the agent to use external CLIs/services. (source: nanobot/skills/README.md, nanobot/skills/*/SKILL.md)

- [`nanobot/skills/README.md`](../nanobot/skills/README.md) (format + skill list) (source: nanobot/skills/README.md)
- Built-in skills: `github`, `weather`, `summarize`, `tmux`, `cron`, `skill-creator` (source: nanobot/skills/README.md)
  - [`nanobot/skills/github/SKILL.md`](../nanobot/skills/github/SKILL.md) (source: nanobot/skills/github/SKILL.md)
  - [`nanobot/skills/weather/SKILL.md`](../nanobot/skills/weather/SKILL.md) (source: nanobot/skills/weather/SKILL.md)
  - [`nanobot/skills/summarize/SKILL.md`](../nanobot/skills/summarize/SKILL.md) (source: nanobot/skills/summarize/SKILL.md)
  - [`nanobot/skills/tmux/SKILL.md`](../nanobot/skills/tmux/SKILL.md) (source: nanobot/skills/tmux/SKILL.md)
  - [`nanobot/skills/cron/SKILL.md`](../nanobot/skills/cron/SKILL.md) (source: nanobot/skills/cron/SKILL.md)
  - [`nanobot/skills/skill-creator/SKILL.md`](../nanobot/skills/skill-creator/SKILL.md) (source: nanobot/skills/skill-creator/SKILL.md)

## 4) Cross-cutting concepts & glossary

Term → meaning → where defined/used.

- **nanobot** → “ultra-lightweight personal AI assistant” with CLI + providers + tools + optional channels. (source: README.md)
- **workspace** → Inference: a local folder of agent-facing templates/instructions (e.g. `AGENTS.md`, `TOOLS.md`, memory/heartbeat) used to guide behavior and persistence. (source: workspace/AGENTS.md, workspace/TOOLS.md, workspace/HEARTBEAT.md, workspace/memory/MEMORY.md)
- **gateway** → A runtime mode that connects nanobot to chat apps/channels (Telegram/Discord/WhatsApp/Feishu) so you can “talk to your nanobot” via messaging apps. (source: README.md#-chat-apps)
- **channels** → Integrations for chat apps (Telegram/Discord/WhatsApp/Feishu) configured under `channels.*` in config, typically with `enabled`, credentials, and `allowFrom`. (source: README.md#-chat-apps, README.md#security)
- **allowFrom** → Channel allow-list (whitelist) for who can interact; recommended to configure for production use. (source: SECURITY.md#2-channel-access-control, README.md#security)
- **restrictToWorkspace** → Security option to restrict agent tools to the workspace directory to reduce out-of-scope access risk. (source: README.md#security)
- **providers** → LLM provider configurations under `providers.*` in `~/.nanobot/config.json` (e.g. OpenRouter/Anthropic/OpenAI/DeepSeek/Groq/Gemini/vLLM). (source: README.md#providers)
- **vLLM** → A way to run local models via an OpenAI-compatible server and configure nanobot to use it. (source: README.md#-local-models-vllm)
- **skills** → Modular packages that extend the agent’s capabilities via `SKILL.md` instructions; nanobot ships a built-in set (github/weather/summarize/tmux/etc.). (source: nanobot/skills/README.md)
- **heartbeat** → A periodic mechanism that checks `HEARTBEAT.md` (every 30 minutes) to run ongoing tasks if present. (source: workspace/HEARTBEAT.md, workspace/AGENTS.md)
- **cron** → Ambiguous in docs: sometimes described as CLI (`nanobot cron ...`), sometimes as an abstract tool call (`cron(action="add", ...)`). (source: README.md#cli-reference, nanobot/skills/cron/SKILL.md)

## 5) User journeys (from docs)

### Journey: “I want to run it locally”

- **Preconditions**: Python ≥ 3.11. (source: README.md)
- **Steps**:
  1. Install nanobot (source install, uv, or PyPI). (source: README.md#-install)
  2. Initialize config with `nanobot onboard`. (source: README.md#-quick-start)
  3. Edit `~/.nanobot/config.json` to add at least one provider API key and set the default model if desired. (source: README.md#-quick-start)
  4. Chat via `nanobot agent -m "..."` (or interactive `nanobot agent`). (source: README.md#-quick-start, README.md#cli-reference)
- **Common pitfalls (mentioned)**:
  - Inference: forgetting to configure the provider API key in `~/.nanobot/config.json` blocks LLM calls. (source: README.md#-quick-start)
  - For production-like usage, consider tool sandboxing (`restrictToWorkspace`). (source: README.md#security)

### Journey: “I want to use a local model”

- **Preconditions**: A running OpenAI-compatible server (example: vLLM). (source: README.md#-local-models-vllm)
- **Steps**:
  1. Start a vLLM server (example command shown). (source: README.md#-local-models-vllm)
  2. Configure provider `vllm` with `apiBase` pointing at your server and a non-empty `apiKey`. (source: README.md#-local-models-vllm)
  3. Set your default model to the vLLM-hosted model, then run `nanobot agent`. (source: README.md#-local-models-vllm)
- **Common pitfalls (mentioned)**:
  - The docs note `apiKey` can be any non-empty string for local servers that don’t need auth. (source: README.md#-local-models-vllm)

### Journey: “I want to talk to it from a chat app”

- **Preconditions**: Channel credentials (token/app ID/app secret/linked device) depending on the channel. (source: README.md#-chat-apps)
- **Steps**:
  1. Choose a channel and configure `channels.<name>` in `~/.nanobot/config.json` (examples provided per channel). (source: README.md#-chat-apps)
  2. (Recommended for safety) Set `allowFrom` to your user ID / phone number / org unit, depending on the channel. (source: README.md#-chat-apps, SECURITY.md#2-channel-access-control)
  3. Run the gateway with `nanobot gateway`. (source: README.md#-chat-apps, README.md#cli-reference)
- **Common pitfalls (mentioned)**:
  - WhatsApp requires Node.js ≥ 18. (source: README.md#whatsapp)
  - Discord requires enabling “MESSAGE CONTENT INTENT”. (source: README.md#discord)
  - Feishu “Long Connection” mode uses WebSocket and the docs emphasize “no public IP required.” (source: README.md#feishu-飞书)

### Journey: “I want to deploy/run it in Docker”

- **Preconditions**: Docker available; config directory on host (`~/.nanobot`). (source: README.md#-docker)
- **Steps**:
  1. Build the image (`docker build -t nanobot .`). (source: README.md#-docker)
  2. Run `onboard` once, mounting `~/.nanobot` into the container. (source: README.md#-docker)
  3. Edit `~/.nanobot/config.json` on the host to add API keys. (source: README.md#-docker)
  4. Run gateway / agent / status via `docker run ...`. (source: README.md#-docker)
- **Common pitfalls (mentioned)**:
  - Mounting `~/.nanobot:/root/.nanobot` is called out as the way to persist config/workspace across restarts. (source: README.md#-docker)

### Journey: “I want to contribute”

- **Preconditions**: Inference: the project expects PR-based contributions (“PRs welcome”). (source: README.md#-contribute--roadmap)
- **Steps**:
  1. Read the repo overview and project structure. (source: README.md#-project-structure)
  2. Pick a roadmap item or improvement area and open a PR. (source: README.md#-contribute--roadmap)
- **Common pitfalls (mentioned)**:
  - Inference: there is no documented local dev/test workflow in Markdown beyond install/run, so contributors may need to inspect code/tests. (source: README.md)

## 6) Gaps, conflicts, and TODOs

### Missing documentation I expected but didn’t find (in Markdown)

- **Contribution workflow**: no `CONTRIBUTING.md` (how to run tests, style, release process, etc.). (source: README.md#-contribute--roadmap)
- **Troubleshooting/runbooks**: no dedicated troubleshooting guide (common failures, logs, “how to debug channel issues”, etc.), though security mentions log monitoring. (source: SECURITY.md#7-production-deployment)
- **Configuration reference**: config is shown by example, but there isn’t a single canonical config schema/reference doc in Markdown. (source: README.md#-quick-start, README.md#configuration)
- **Architecture narrative**: README has an architecture image, but no written architecture walkthrough in Markdown. (source: README.md#-architecture)

### Conflicting / potentially confusing instructions across docs

- **Cron scheduling interface mismatch**: README documents cron via CLI commands; the `cron` skill documents cron as a tool-call interface. These may be describing different layers, but the docs don’t connect them explicitly. (source: README.md#cli-reference, nanobot/skills/cron/SKILL.md)\n+  - Quote: `cron(action=\"add\", message=\"Time to take a break!\", every_seconds=1200)` (source: nanobot/skills/cron/SKILL.md)\n+  - Quote: `nanobot cron add --name \"daily\" --message \"Good morning!\" --cron \"0 9 * * *\"` (source: README.md#cli-reference)

### Stale hints / TODO signals in docs

- **Workspace templates are placeholders**: `workspace/USER.md` and `workspace/memory/MEMORY.md` are mostly templates rather than “filled-in” guidance, so readers may not know what a “good” completed version looks like. (source: workspace/USER.md, workspace/memory/MEMORY.md)

## 7) Suggested next docs to create (minimal set)

These are the smallest additions that would make the repo meaningfully more onboardable for users and contributors, based on gaps above. (Inference: prioritized by what’s missing vs what’s already covered in `README.md` and `SECURITY.md`.) (source: README.md, SECURITY.md)

### `CONTRIBUTING.md`

- **Intent**: Make “PRs welcome” actionable with a consistent dev/test workflow. (source: README.md#-contribute--roadmap)
- **Outline**:
  - Project goals (small/readable, research-ready) (source: README.md#key-features-of-nanobot)
  - Supported Python versions + env setup
  - Installing for development (`pip install -e .`) (source: README.md#-install)
  - Running tests (point to `tests/` scripts; document expected commands) (Inference: tests exist but not documented) (source: README.md, SECURITY.md)
  - Code style/formatting expectations (Inference) (source: README.md)
  - How to add/update a provider/channel/tool (high-level pointers) (Inference) (source: README.md#-project-structure)
  - Security expectations (never commit keys; least privilege) (source: SECURITY.md#1-api-key-management)
  - PR checklist + review expectations (Inference) (source: README.md)

### `docs/CONFIGURATION.md`

- **Intent**: Provide a canonical reference for `~/.nanobot/config.json` structure beyond examples. (source: README.md#-quick-start, README.md#configuration)
- **Outline**:
  - Config file location + how it’s created (`nanobot onboard`) (source: README.md#-quick-start)
  - Providers: required fields by provider (apiKey/apiBase/model) (source: README.md#providers, README.md#-local-models-vllm)
  - Channels: required fields + `allowFrom` semantics (source: README.md#-chat-apps, SECURITY.md#2-channel-access-control)
  - Tools config (web search key, restrictToWorkspace) (source: README.md#-quick-start, README.md#security)
  - Security defaults and recommended production overrides (source: SECURITY.md#security-checklist)
  - Examples: minimal configs for (1) OpenRouter-only (2) vLLM-local (3) Telegram gateway (source: README.md#-quick-start, README.md#-local-models-vllm, README.md#telegram-recommended)

### `docs/DEPLOYMENT.md`

- **Intent**: Combine Docker + “production deployment” security guidance into one operational narrative. (source: README.md#-docker, SECURITY.md#7-production-deployment)
- **Outline**:
  - Deployment options: Docker vs VM vs bare-metal (source: README.md#-docker, SECURITY.md#7-production-deployment)
  - Non-root + dedicated user recommendations (source: SECURITY.md#7-production-deployment)
  - Filesystem permissions for `~/.nanobot` and WhatsApp auth (source: SECURITY.md#1-api-key-management, SECURITY.md#5-network-security)
  - Channel hardening: `allowFrom`, rate limiting guidance (source: SECURITY.md#2-channel-access-control, SECURITY.md#known-limitations)
  - Logging/monitoring suggestions (source: SECURITY.md#7-production-deployment)
  - Upgrade strategy (dependencies, release notes) (source: SECURITY.md#6-dependency-security)

### `docs/TROUBLESHOOTING.md`

- **Intent**: Collect common failure modes implied by docs into a quick diagnostic flow. (Inference) (source: README.md, SECURITY.md)
- **Outline**:
  - “nanobot won’t start” (Python/version issues) (Inference) (source: README.md)
  - “LLM calls fail” (missing/invalid provider keys) (Inference) (source: README.md#-quick-start)
  - “gateway runs but no messages” (channel token/intents/allowFrom) (Inference) (source: README.md#discord, SECURITY.md#2-channel-access-control)
  - “WhatsApp login issues” (Node version, QR linking, auth folder permissions) (Inference) (source: README.md#whatsapp, SECURITY.md#5-network-security)
  - “Docker config not persisting” (volume mount) (Inference) (source: README.md#-docker)
  - Security incident checklist pointer (source: SECURITY.md#10-incident-response)

