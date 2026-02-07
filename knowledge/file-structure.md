# File & Folder Structure Overview

This document is a **structural + semantic map** of the repository: what lives where, why it exists, and how responsibilities split across the filesystem.

## 1) High-level layout

- **Directory tree used for this analysis (depth-limited; not exhaustive)**

  - `bridge/`
    - `package.json`
    - `tsconfig.json`
    - `src/` (`index.ts`, `server.ts`, `whatsapp.ts`, `types.d.ts`)
  - `case/` (`*.gif`)
  - `knowledge/` (`overview.md`, `file-structure.md`)
  - `nanobot/`
    - package entry points (`__init__.py`, `__main__.py`)
    - `agent/` (`loop.py`, `context.py`, `memory.py`, `skills.py`, `subagent.py`, `tools/…`)
    - `bus/` (`events.py`, `queue.py`)
    - `channels/` (`base.py`, `manager.py`, `telegram.py`, `discord.py`, `whatsapp.py`, `feishu.py`)
    - `cli/` (`commands.py`)
    - `config/` (`loader.py`, `schema.py`)
    - `cron/` (`service.py`, `types.py`)
    - `heartbeat/` (`service.py`)
    - `providers/` (`base.py`, `litellm_provider.py`, `transcription.py`)
    - `session/` (`manager.py`)
    - `skills/` (bundled skills: `*/SKILL.md`, plus `README.md`, scripts under `tmux/`)
    - `utils/` (`helpers.py`)
  - `tests/` (`test_tool_validation.py`, `test_docker.sh`)
  - `workspace/` (`AGENTS.md`, `TOOLS.md`, `HEARTBEAT.md`, `SOUL.md`, `USER.md`, `memory/MEMORY.md`)
  - Top-level build/docs assets
    - `pyproject.toml`, `Dockerfile`, `.gitignore`, `.dockerignore`
    - `README.md`, `SECURITY.md`, `COMMUNICATION.md`
    - `nanobot_arch.png`, `nanobot_logo.png`
    - `core_agent_lines.sh`

- **Main “zones” (Observed)**
  - **Runtime product code (Python)**: `nanobot/` (source: `nanobot/`)
  - **Integration bridge (Node/TypeScript)**: `bridge/` (WhatsApp Web bridge) (source: `bridge/`)
  - **Tests**: `tests/` (source: `tests/`)
  - **Operator / agent-workspace templates**: `workspace/` (shipped templates for `~/.nanobot/workspace`) (source: `workspace/`, `nanobot/cli/commands.py`)
  - **Repository knowledge/docs**: `README.md`, `SECURITY.md`, `knowledge/`, `COMMUNICATION.md` (source: `README.md`, `SECURITY.md`, `knowledge/overview.md`, `COMMUNICATION.md`)
  - **Demo media assets**: `case/` and image files in repo root (source: `case/`, `nanobot_arch.png`, `nanobot_logo.png`)

- **Organizing principle (Inference; supported by names/docstrings)**
  - Primarily **layered / component-based**: agent core (`agent/`), I/O integrations (`channels/`, `bridge/`), infrastructure services (`cron/`, `heartbeat/`), messaging bus (`bus/`), configuration (`config/`), CLI (`cli/`), plus shared utilities (`utils/`). (source: `nanobot/`, `README.md#📁-Project-Structure`)

## 2) Top-level directory responsibilities

### `bridge/`

- **Path**: `bridge/`
- **Primary responsibility**: Node/TypeScript **WhatsApp Web bridge** that connects to the Python runtime over WebSocket. (source: `bridge/src/index.ts`, `bridge/src/server.ts`, `bridge/package.json`)
- **What belongs here**
  - Bridge server and WhatsApp client wiring (`src/…`) (source: `bridge/src/`)
  - Bridge build config (`package.json`, `tsconfig.json`) (source: `bridge/`)
- **What explicitly should NOT belong here**
  - Python agent logic or CLI code (belongs in `nanobot/`) (Inference; source boundaries: `nanobot/` vs `bridge/`)
  - Built artifacts like `dist/` if they can be generated (Inference; typical TS build output; `Dockerfile` builds it) (source: `Dockerfile`)
- **Who typically touches this**: Integration engineers / maintainers working on WhatsApp support; occasionally app devs debugging message flow. (Inference; source: WhatsApp docs in `README.md`, bridge source)

### `case/`

- **Path**: `case/`
- **Primary responsibility**: Demo / showcase media (GIFs) used by the README. (source: `README.md`, `case/`)
- **What belongs here**
  - Short UX demos and screenshots (source: `case/`)
- **What explicitly should NOT belong here**
  - Core source code, tests, or build artifacts (Inference)
- **Who typically touches this**: Docs/marketing contributors, maintainers updating README visuals. (Inference)

### `knowledge/`

- **Path**: `knowledge/`
- **Primary responsibility**: Repository-internal “knowledge documents” (maps, analyses) intended for contributors and agents. (source: `knowledge/overview.md`)
- **What belongs here**
  - Curated documentation maps, structural analyses, architectural notes (source: `knowledge/overview.md`)
- **What explicitly should NOT belong here**
  - Runtime code and configs (Inference)
- **Who typically touches this**: Contributors documenting the repo; maintainers keeping docs aligned with code. (Inference)

### `nanobot/`

- **Path**: `nanobot/`
- **Primary responsibility**: The **Python package** implementing the agent runtime: CLI, agent loop, tools, providers, channels, scheduling, and persistence. (source: `pyproject.toml`, `nanobot/cli/commands.py`, `nanobot/agent/loop.py`)
- **What belongs here**
  - Core runtime components (`agent/`, `bus/`, `session/`, etc.) (source: `nanobot/`)
  - Bundled “skills” shipped with the package (`nanobot/skills/…`) (source: `pyproject.toml`, `nanobot/skills/README.md`)
- **What explicitly should NOT belong here**
  - Large external dependencies or vendored libraries (Inference; packaging is via `pyproject.toml` and pip/uv)
  - Repo-specific contributor docs (belongs at root `README.md` or `knowledge/`) (Inference)
- **Who typically touches this**: Application developers and maintainers implementing agent behavior and integrations. (Inference)

### `tests/`

- **Path**: `tests/`
- **Primary responsibility**: Automated checks (Python unit tests + a Docker smoke test script). (source: `tests/test_tool_validation.py`, `tests/test_docker.sh`)
- **What belongs here**
  - Unit tests and integration/smoke scripts (source: `tests/`)
- **What explicitly should NOT belong here**
  - Production runtime code (Inference)
- **Who typically touches this**: Contributors adding features/fixes; maintainers validating releases. (Inference)

### `workspace/`

- **Path**: `workspace/`
- **Primary responsibility**: **Template workspace files** intended to be copied/created under the user’s `~/.nanobot/workspace`. (source: `workspace/*.md`, `nanobot/cli/commands.py`, `nanobot/agent/context.py`)
- **What belongs here**
  - Agent instruction and personalization templates (`AGENTS.md`, `SOUL.md`, `USER.md`) (source: `workspace/AGENTS.md`, `workspace/SOUL.md`, `workspace/USER.md`)
  - Tool and process docs used at runtime for prompt construction / guidance (`TOOLS.md`, `HEARTBEAT.md`, `memory/MEMORY.md`) (source: `workspace/TOOLS.md`, `workspace/HEARTBEAT.md`, `workspace/memory/MEMORY.md`)
- **What explicitly should NOT belong here**
  - Package code (belongs in `nanobot/`) (Inference)
  - User-specific secrets (belongs under `~/.nanobot/config.json`, not committed) (Inference; source: `README.md`, `SECURITY.md`)
- **Who typically touches this**: Maintainers curating defaults; advanced users customizing their local workspace (locally, not necessarily in this repo). (Inference; source: `nanobot/cli/commands.py`, `README.md`)

## 3) Nested structure (drill-down)

### `nanobot/` package entry points

- **`nanobot/__main__.py`**
  - Role: `python -m nanobot` entrypoint that delegates to the CLI app. (source: `nanobot/__main__.py`)
- **`nanobot/__init__.py`**
  - Role: package metadata like version and logo used by CLI UX. (source: `nanobot/__init__.py`)
  - Note: version here may not match the package version in `pyproject.toml` (see “Smells”). (source: `nanobot/__init__.py`, `pyproject.toml`)

### `nanobot/cli/` (technical layer: CLI / operator interface)

- **Role**: Defines user-facing commands (`nanobot onboard`, `nanobot agent`, `nanobot gateway`, `nanobot cron …`, `nanobot channels …`, `nanobot status`). (source: `nanobot/cli/commands.py`, `pyproject.toml`)
- **How it relates**
  - Orchestrates and wires together core components: config, bus, provider, agent loop, channel manager, cron, heartbeat. (source: `nanobot/cli/commands.py`)
- **Key files/patterns**
  - `commands.py` contains command groups and the main wiring graph. (source: `nanobot/cli/commands.py`)
- **Represents**: deployment/runtime concern + integration boundary (CLI-to-core). (Inference; source: `nanobot/cli/commands.py`)

### `nanobot/config/` (cross-cutting: configuration + schema)

- **Role**: Defines the configuration model (`schema.py`) and loading/saving + migrations (`loader.py`). (source: `nanobot/config/schema.py`, `nanobot/config/loader.py`)
- **How it relates**
  - CLI and runtime read config from `~/.nanobot/config.json` and convert between camelCase in JSON and snake_case in code. (source: `nanobot/config/loader.py`)
  - Config also encodes security posture (`tools.restrict_to_workspace`, channel `allow_from`). (source: `nanobot/config/schema.py`, `README.md`, `SECURITY.md`)
- **Key files/patterns**
  - `schema.py`: Pydantic models for channels, providers, tools, defaults; helper methods for selecting provider keys based on model name. (source: `nanobot/config/schema.py`)
  - `loader.py`: “best effort” migration and key conversion (camel↔snake). (source: `nanobot/config/loader.py`)
- **Represents**: cross-cutting layer; also a **policy boundary** (restrict tool access). (Inference; source: `nanobot/config/schema.py`, `nanobot/agent/loop.py`)

### `nanobot/bus/` (technical layer: message routing)

- **Role**: Decouples chat channels from the agent core via async queues. (source: `nanobot/bus/queue.py`)
- **How it relates**
  - Channels push `InboundMessage`s; agent loop consumes them and pushes `OutboundMessage`s. (source: `nanobot/bus/events.py`, `nanobot/bus/queue.py`, `nanobot/agent/loop.py`)
- **Key files**
  - `events.py`: typed message shapes; defines `session_key` convention (`channel:chat_id`). (source: `nanobot/bus/events.py`)
  - `queue.py`: the actual queue-based bus implementation. (source: `nanobot/bus/queue.py`)
- **Represents**: integration boundary (channels ↔ agent). (Observed)

### `nanobot/session/` (runtime concern: persistence of conversation history)

- **Role**: Stores conversation history in JSONL files and provides LLM-formatted history slices. (source: `nanobot/session/manager.py`)
- **How it relates**
  - `AgentLoop` uses `SessionManager.get_or_create()` and saves after each turn. (source: `nanobot/agent/loop.py`, `nanobot/session/manager.py`)
  - Storage lives under `~/.nanobot/sessions` rather than inside the workspace directory. (Observed; source: `nanobot/session/manager.py`)
- **Key patterns**
  - JSONL format with a metadata header line (`_type: metadata`). (source: `nanobot/session/manager.py`)
- **Represents**: runtime persistence concern. (Observed)

### `nanobot/agent/` (core domain: agent “thinking loop” + context assembly)

- **Role**: Implements the core LLM ↔ tool execution loop and prompt/context construction. (source: `nanobot/agent/loop.py`, `nanobot/agent/context.py`)
- **How it relates**
  - Depends on provider abstraction (`providers/`), tool registry (`agent/tools/`), sessions (`session/`), and the bus (`bus/`). (source: `nanobot/agent/loop.py`)
- **Key files/patterns**
  - `loop.py`: registers default tools; iterates tool calls until final response or max iterations; routes system messages (subagent announcements) specially. (source: `nanobot/agent/loop.py`)
  - `context.py`: builds system prompt from identity + “bootstrap files” + memory + skill summaries, and attaches session info. (source: `nanobot/agent/context.py`)
  - `memory.py`: reads/writes persistent memory under `workspace/memory/` and provides context snippets. (source: `nanobot/agent/memory.py`)
  - `skills.py`: progressive skill loading: include “always” skills in full; list others as an index with availability based on dependencies. (source: `nanobot/agent/skills.py`, `nanobot/skills/README.md`)
  - `subagent.py`: runs background subagents with a reduced toolset and reports back via the bus. (source: `nanobot/agent/subagent.py`)
- **Represents**: domain concept (agent behavior) + technical layer (LLM/tool protocol). (Inference)

### `nanobot/agent/tools/` (technical layer: tool surface area & safety boundary)

- **Role**: Defines the “capabilities” the LLM can invoke (file ops, shell exec, web, messaging, spawning, cron). (source: `nanobot/agent/tools/*.py`, `workspace/TOOLS.md`)
- **How it relates**
  - `AgentLoop` registers tools and exposes schemas to providers; executes tool calls and appends tool results to the message stream. (source: `nanobot/agent/loop.py`, `nanobot/agent/tools/registry.py`)
  - Some tools apply safety/policy restrictions derived from config (e.g., restrict-to-workspace). (source: `nanobot/agent/loop.py`, `nanobot/agent/tools/filesystem.py`, `nanobot/agent/tools/shell.py`)
- **Key files/patterns**
  - `base.py`: JSON-schema parameter validation used by the registry. (source: `nanobot/agent/tools/base.py`)
  - `registry.py`: registers tools and standardizes execution results as strings. (source: `nanobot/agent/tools/registry.py`)
  - `filesystem.py`: `read_file` / `write_file` / `edit_file` / `list_dir`, with optional `allowed_dir` enforcement. (source: `nanobot/agent/tools/filesystem.py`)
  - `shell.py`: `exec` tool with deny-pattern guardrails + optional path traversal / workspace restriction. (source: `nanobot/agent/tools/shell.py`, `SECURITY.md`)
  - `web.py`: `web_search` (Brave API) + `web_fetch` (Readability extraction) with URL validation and output truncation. (source: `nanobot/agent/tools/web.py`)
  - `message.py`: sends outbound messages through the bus for a specific channel/chat context. (source: `nanobot/agent/tools/message.py`)
  - `spawn.py`: starts a `SubagentManager` job. (source: `nanobot/agent/tools/spawn.py`, `nanobot/agent/subagent.py`)
  - `cron.py`: schedules jobs through `CronService`, binding to the current session context for delivery. (source: `nanobot/agent/tools/cron.py`, `nanobot/cron/service.py`)
- **Represents**: integration boundary and a security boundary. (Inference; source: `nanobot/agent/tools/shell.py`, `nanobot/agent/tools/filesystem.py`, `README.md#Security`, `SECURITY.md`)

### `nanobot/providers/` (integration boundary: LLM providers + adapters)

- **Role**: Abstracts LLM chat API calls behind a consistent interface (`LLMProvider`) and provides a concrete multi-provider implementation via LiteLLM. (source: `nanobot/providers/base.py`, `nanobot/providers/litellm_provider.py`)
- **How it relates**
  - Agent core depends only on `LLMProvider` interface. (source: `nanobot/agent/loop.py`, `nanobot/providers/base.py`)
  - Provider selection is largely driven by config model names and keys. (source: `nanobot/config/schema.py`, `nanobot/providers/litellm_provider.py`)
- **Key files/patterns**
  - `base.py`: typed response model including tool calls. (source: `nanobot/providers/base.py`)
  - `litellm_provider.py`: environment-variable mapping + model prefix normalization + error-as-content handling. (source: `nanobot/providers/litellm_provider.py`)
  - `transcription.py`: Groq Whisper transcription client used by at least the Telegram channel for voice/audio messages. (source: `nanobot/providers/transcription.py`, `nanobot/channels/telegram.py`)
- **Represents**: integration boundary (LLM APIs). (Observed)

### `nanobot/channels/` (integration boundary: chat apps)

- **Role**: Implements chat “front-ends” (Telegram/Discord/WhatsApp/Feishu) and connects them to the bus. (source: `nanobot/channels/manager.py`, `README.md#💬-Chat-Apps`)
- **How it relates**
  - `ChannelManager` instantiates enabled channels from config and runs them concurrently with agent loop. (source: `nanobot/channels/manager.py`, `nanobot/cli/commands.py`)
  - Channels use `BaseChannel._handle_message()` to enforce allow-lists (`allow_from`) and forward inbound messages to the bus. (source: `nanobot/channels/base.py`)
- **Key files/patterns**
  - `manager.py`: dynamic channel initialization with graceful “optional dependency” behavior. (source: `nanobot/channels/manager.py`)
  - `base.py`: abstract channel contract + shared allow-list enforcement + bus forwarding helper. (source: `nanobot/channels/base.py`)
  - `telegram.py`: long-polling Telegram bot; downloads media to `~/.nanobot/media/` and optionally transcribes voice/audio via Groq. (source: `nanobot/channels/telegram.py`, `nanobot/providers/transcription.py`)
  - `whatsapp.py`: connects to the Node bridge URL (`channels.whatsapp.bridge_url`) over WebSocket; inbound “message/status/qr/error” events; outbound “send” commands. (source: `nanobot/channels/whatsapp.py`, `nanobot/config/schema.py`, `bridge/src/server.ts`)
- **Represents**: integration boundary (external chat networks) + runtime concern. (Observed)

### `nanobot/cron/` (deployment/runtime concern: scheduled tasks)

- **Role**: Stores scheduled jobs in `~/.nanobot` data and executes them on timers; optionally delivers results back to channels. (source: `nanobot/cron/service.py`, `nanobot/cli/commands.py`)
- **How it relates**
  - CLI command `nanobot cron …` manages jobs; runtime `gateway` starts `CronService` and routes execution through `AgentLoop.process_direct`. (source: `nanobot/cli/commands.py`)
  - Agent tool `cron` is another entry point to schedule jobs programmatically from the LLM side. (source: `nanobot/agent/tools/cron.py`)
- **Key files**
  - `service.py`: timer scheduling, disk store read/write, job lifecycle. (source: `nanobot/cron/service.py`)
  - `types.py`: data models for job/schedule/payload (not reviewed in depth here). (Inference; source: file presence `nanobot/cron/types.py`)
- **Represents**: runtime concern; also an integration boundary (agent ↔ timer). (Inference)

### `nanobot/heartbeat/` (runtime concern: periodic “wake up” mechanism)

- **Role**: Every interval (default 30 minutes), checks `HEARTBEAT.md` in the workspace and triggers an agent turn if there is actionable content. (source: `nanobot/heartbeat/service.py`, `workspace/HEARTBEAT.md`)
- **How it relates**
  - Gateway wires it to a callback that calls `AgentLoop.process_direct`. (source: `nanobot/cli/commands.py`)
  - The file-based task list is part of the workspace template docs. (source: `workspace/HEARTBEAT.md`)
- **Key files**
  - `service.py`: heartbeat prompt token, “empty detection” heuristics, scheduling loop. (source: `nanobot/heartbeat/service.py`)
- **Represents**: runtime concern; “proactive agent” boundary. (Inference; source: `nanobot/heartbeat/service.py`)

### `nanobot/skills/` (domain concept: skill library; packaging concern)

- **Role**: Bundled “skills” (instructional `SKILL.md` files) that teach the agent how to use external tools/services and follow project-specific workflows. (source: `nanobot/skills/README.md`)
- **How it relates**
  - `SkillsLoader` (in `nanobot/agent/skills.py`) reads from both workspace skills and bundled skills, and surfaces availability based on dependency checks. (source: `nanobot/agent/skills.py`)
  - Packaged into wheels/sdist per `pyproject.toml` include rules. (source: `pyproject.toml`)
- **Key patterns**
  - One skill per directory with `SKILL.md` and optional scripts/assets. (source: `nanobot/skills/README.md`)
- **Represents**: domain concept + extension mechanism. (Observed)

### `workspace/` (repo templates that become runtime prompt inputs)

- **Role**: The “bootstrap files” and operator guidance that the agent uses to construct its system prompt and ongoing behavior. (source: `nanobot/agent/context.py`, `workspace/TOOLS.md`, `workspace/AGENTS.md`)
- **How it relates**
  - `ContextBuilder.BOOTSTRAP_FILES` includes `AGENTS.md`, `SOUL.md`, `USER.md`, `TOOLS.md`, and `IDENTITY.md` if present. (source: `nanobot/agent/context.py`)
  - `nanobot onboard` creates a minimal subset of these files if missing (notably: it does not mention `TOOLS.md` in the hard-coded templates). (source: `nanobot/cli/commands.py`)
- **Represents**: deployment/runtime concern (user workspace) + behavior boundary (prompt injection surface). (Inference; source: `nanobot/agent/context.py`)

### `bridge/src/` (integration boundary: WhatsApp Web ↔ Python)

- **Role**: WebSocket server + WhatsApp client wrapper; broadcasts inbound messages/QR/status to Python; accepts “send” commands from Python. (source: `bridge/src/index.ts`, `bridge/src/server.ts`)
- **Key files**
  - `index.ts`: process entrypoint; config via env (`BRIDGE_PORT`, `AUTH_DIR`). (source: `bridge/src/index.ts`)
  - `server.ts`: WebSocket protocol and broadcast fanout to connected Python clients. (source: `bridge/src/server.ts`)
- **Represents**: integration boundary (Node WhatsApp stack) and security surface (auth data directory). (Inference; source: `bridge/src/index.ts`, `SECURITY.md` WhatsApp notes)

## 4) Architectural signals inferred from structure

- **Observed**
  - **Event/queue decoupling** between I/O channels and core agent via `MessageBus` (`nanobot/bus/`). (source: `nanobot/bus/queue.py`, `nanobot/agent/loop.py`)
  - **Tool-plugin architecture**: tools are registered dynamically, exposed as JSON schemas, and executed by name (`nanobot/agent/tools/`). (source: `nanobot/agent/tools/registry.py`, `nanobot/agent/tools/base.py`, `nanobot/agent/loop.py`)
  - **Provider abstraction**: core loop depends on `LLMProvider`, with LiteLLM as a multi-provider adapter. (source: `nanobot/providers/base.py`, `nanobot/providers/litellm_provider.py`, `nanobot/agent/loop.py`)
  - **File-based workspace model**: runtime behavior is shaped by a workspace directory containing bootstrap docs and memory. (source: `nanobot/agent/context.py`, `nanobot/agent/memory.py`, `workspace/`)
  - **Scheduling services** as first-class runtime components: cron (`nanobot/cron/`) and heartbeat (`nanobot/heartbeat/`) are started in gateway mode. (source: `nanobot/cli/commands.py`)

- **Inference**
  - The structure resembles a **“small clean/hexagonal core”**: agent core depends on abstractions (provider interface, bus messages), while integrations live at the edges (`channels/`, `bridge/`). (source: `nanobot/agent/loop.py`, `nanobot/providers/base.py`, `nanobot/bus/events.py`, `nanobot/channels/manager.py`, `bridge/`)
  - **Seams / boundaries** are clear at:
    - Agent/tool boundary: `nanobot/agent/tools/` (source: `nanobot/agent/tools/…`)
    - External network boundary: `nanobot/channels/`, `nanobot/agent/tools/web.py`, `bridge/` (source: `nanobot/channels/`, `nanobot/agent/tools/web.py`, `bridge/`)
    - Persistence boundary: `nanobot/session/`, `nanobot/cron/` store under `~/.nanobot` (source: `nanobot/session/manager.py`, `nanobot/cron/service.py`)

## 5) Cross-cutting folders and patterns

- **Configuration**
  - Config file location is **outside the repo**: `~/.nanobot/config.json` (source: `nanobot/config/loader.py`, `README.md`)
  - Config schema defines security knobs (`tools.restrict_to_workspace`) and allow-lists (`channels.*.allow_from`). (source: `nanobot/config/schema.py`, `SECURITY.md`)

- **Logging / telemetry**
  - Runtime uses `loguru` across components (`agent`, `bus`, `cron`, `heartbeat`, `channels`). (source: `nanobot/agent/loop.py`, `nanobot/bus/queue.py`, `nanobot/cron/service.py`, `nanobot/heartbeat/service.py`, `nanobot/channels/manager.py`)

- **Error handling**
  - Tool execution generally returns **stringified errors** rather than raising, to keep the LLM loop moving. (source: `nanobot/agent/tools/registry.py`, `nanobot/agent/tools/*`)
  - Provider errors return as “content” (`LLMResponse(content="Error calling LLM: …")`). (source: `nanobot/providers/litellm_provider.py`)

- **Shared utilities**
  - `nanobot/utils/helpers.py` centralizes `~/.nanobot` path helpers and safe filename logic. (source: `nanobot/utils/helpers.py`)

- **Build / packaging**
  - Python packaging is via `pyproject.toml` + hatchling; skills and bridge are explicitly included in distributions. (source: `pyproject.toml`)
  - Docker image installs Node.js (WhatsApp bridge requirement) and builds the bridge during image build. (source: `Dockerfile`)

- **Tests**
  - Unit tests validate JSON-schema param validation behavior for tools and registry-level error surfacing. (source: `tests/test_tool_validation.py`)
  - Docker smoke test validates `onboard` and `status` flows in a container. (source: `tests/test_docker.sh`)

## 6) Ownership & change impact guide

### Agent core (`nanobot/agent/`)

- **If you change this, what else is likely affected?**
  - Tool invocation protocol, safety posture, prompt construction, and all channels (since all message flows converge here). (source: `nanobot/agent/loop.py`, `nanobot/agent/context.py`)
- **Typical dependency direction**
  - `agent/` depends on `providers/`, `bus/`, `session/`, `agent/tools/`, and indirectly config-driven policy. (source: `nanobot/agent/loop.py`)
- **Risk level**: **High**

### Tools (`nanobot/agent/tools/`)

- **Impact**
  - Affects what the LLM can do, safety constraints, and how errors/results are represented to the model. (source: `nanobot/agent/tools/*`)
- **Dependency direction**
  - Tools are depended on by `AgentLoop`; some tools depend on `cron/` or `bus/`. (source: `nanobot/agent/loop.py`, `nanobot/agent/tools/cron.py`, `nanobot/agent/tools/message.py`)
- **Risk level**: **High** for `exec`/filesystem; **Medium** for web/message/spawn/cron.

### Channels (`nanobot/channels/` + `bridge/` for WhatsApp)

- **Impact**
  - Changes affect inbound/outbound message formatting, authentication, and delivery reliability per platform. (source: `nanobot/channels/manager.py`, `bridge/src/server.ts`)
- **Dependency direction**
  - Channels depend on `bus/` and config; agent core should not depend on specific channels. (Inference; source: `nanobot/channels/manager.py`, `nanobot/bus/queue.py`)
- **Risk level**: **Medium–High** (external API fragility + auth flows)

### Config (`nanobot/config/`)

- **Impact**
  - Breaks startup, provider selection, channel enabling, and security restrictions. (source: `nanobot/config/schema.py`, `nanobot/config/loader.py`, `nanobot/cli/commands.py`)
- **Dependency direction**
  - Most runtime components read config; schema changes ripple broadly. (source: `nanobot/cli/commands.py`)
- **Risk level**: **High**

### Scheduling (`nanobot/cron/`, `nanobot/heartbeat/`)

- **Impact**
  - Affects background execution and potential message delivery side effects. (source: `nanobot/cli/commands.py`, `nanobot/cron/service.py`, `nanobot/heartbeat/service.py`)
- **Dependency direction**
  - CLI wires these into the agent; cron can publish outbound messages via the bus (via callback in gateway wiring). (source: `nanobot/cli/commands.py`)
- **Risk level**: **Medium**

### Persistence (`nanobot/session/`, memory under workspace)

- **Impact**
  - Conversation continuity and how much context the model sees. (source: `nanobot/session/manager.py`, `nanobot/agent/memory.py`)
- **Dependency direction**
  - Agent depends on sessions; memory is pulled into prompts by `ContextBuilder`. (source: `nanobot/agent/loop.py`, `nanobot/agent/context.py`)
- **Risk level**: **Medium**

### Workspace templates (`workspace/`)

- **Impact**
  - Changes can significantly alter agent behavior and tool usage (prompt content). (source: `nanobot/agent/context.py`, `workspace/TOOLS.md`)
- **Dependency direction**
  - Used by prompt construction; independent of runtime code but has behavioral coupling. (Inference; source: `nanobot/agent/context.py`)
- **Risk level**: **Medium–High** (prompt injection / behavior drift)

## 7) Smells, inconsistencies, and risks

- **Version source inconsistency**
  - `pyproject.toml` declares version `0.1.3.post4`, but `nanobot/__init__.py` sets `__version__ = "0.1.0"`. (source: `pyproject.toml`, `nanobot/__init__.py`)
  - Risk: users/CLI may display a misleading version, complicating support and debugging. (Inference)

- **Bootstrap file mismatch / ambiguity**
  - `ContextBuilder.BOOTSTRAP_FILES` includes `IDENTITY.md`, but `nanobot onboard` only creates `AGENTS.md`, `SOUL.md`, `USER.md` (+ `memory/MEMORY.md`), and the repo templates include `TOOLS.md`/`HEARTBEAT.md` but onboard’s hardcoded templates do not mention them. (source: `nanobot/agent/context.py`, `nanobot/cli/commands.py`, `workspace/TOOLS.md`, `workspace/HEARTBEAT.md`)
  - Risk: different installs may have materially different prompt inputs depending on how the workspace is created. (Inference)

- **Docs naming drift**
  - README shows config key `restrictToWorkspace` under `tools.restrictToWorkspace` (camelCase in JSON), while code uses `restrict_to_workspace` internally and migrates older `tools.exec.restrictToWorkspace` to `tools.restrictToWorkspace`. This is handled, but it’s easy to get wrong when hand-editing configs. (source: `README.md`, `nanobot/config/loader.py`, `nanobot/config/schema.py`)

- **`core_agent_lines.sh` portability**
  - Script uses `find … -exec cat` and `xargs cat`, which assumes GNU-ish tooling and a POSIX shell environment. (source: `core_agent_lines.sh`)
  - Risk: may not work consistently on all platforms (Inference).

- **Minor naming/typo signals**
  - `case/scedule.gif` appears misspelled (“schedule”). (source: `case/`)

## 8) Suggested structural improvements (optional)

- **Align version metadata**
  - **Problem**: Version defined in two places appears inconsistent (`pyproject.toml` vs `nanobot/__init__.py`). (source: `pyproject.toml`, `nanobot/__init__.py`)
  - **Proposed change**: Single source of truth (e.g., set `__version__` from package metadata or update `__init__.py` during release). (Inference)
  - **Expected benefit**: Correct version reporting in CLI/logs; easier debugging/support. (Inference)
  - **Migration risk**: Low (Inference)

- **Make workspace/bootstrap template story explicit**
  - **Problem**: There are repo templates in `workspace/`, but `onboard` generates only a subset and `ContextBuilder` expects additional files (`TOOLS.md`, maybe `IDENTITY.md`). (source: `workspace/`, `nanobot/cli/commands.py`, `nanobot/agent/context.py`)
  - **Proposed change**: Either (a) have `onboard` copy from `workspace/` templates, or (b) document the expected bootstrap file set and remove/adjust unused entries. (Inference)
  - **Expected benefit**: Reproducible agent behavior across installations; fewer “it works on my machine” prompt differences. (Inference)
  - **Migration risk**: Medium (prompt changes can alter behavior). (Inference)

