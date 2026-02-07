# Local development

This doc explains how to set up a local dev environment and run **nanobot** from this repository.

## Prerequisites

- **Python**: 3.11+ (required)
- **Git**
- **(Optional) uv**: for fast installs (the Docker image uses it)
- **(Optional, WhatsApp only) Node.js + npm**:
  - The repo’s `bridge/package.json` requires **Node >= 20**
  - The CLI error message and README mention Node >= 18, but **Node 20 is the safest choice**

## Setup (Python)

### Option A: `venv` + `pip`

From the repo root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
pip install -e ".[dev]"
```

### Option B: `uv`

From the repo root:

```bash
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"
```

## Initialize configuration

Run:

```bash
nanobot onboard
```

This creates:

- `~/.nanobot/config.json`
- `~/.nanobot/workspace/` (with initial bootstrap files)

Then edit `~/.nanobot/config.json` and add at least one provider API key (example: `providers.openrouter.apiKey`), and optionally set `agents.defaults.model`.

### `providers.*.apiBase` (what it is)

In `~/.nanobot/config.json`, each provider has:

- `apiKey`: the credential for that provider
- `apiBase`: the **base URL (endpoint root)** for the provider’s API (usually leave as `null`)

If `apiBase` is `null`, nanobot uses the provider’s default base URL via its provider adapter. Set `apiBase` **only** if you want to route requests through:

- a proxy / gateway,
- a self-hosted OpenAI-compatible server (e.g. vLLM),
- or a non-default endpoint.

Example (vLLM / local OpenAI-compatible server):

```json
{
  "providers": {
    "vllm": {
      "apiKey": "dummy",
      "apiBase": "http://localhost:8000/v1"
    }
  }
}
```

### (Optional) Use a repo-local workspace during development

By default, nanobot uses `~/.nanobot/workspace`. If you want an isolated workspace per checkout, set:

- `agents.defaults.workspace` in `~/.nanobot/config.json`

Example:

```json
{
  "agents": {
    "defaults": {
      "workspace": "/absolute/path/to/your/checkout/.nanobot-workspace"
    }
  }
}
```

## Run nanobot (from this repo)

After `pip install -e ".[dev]"` (or `pip install -e .`), the `nanobot` CLI will run your local working tree.

### CLI agent (chat)

One-shot:

```bash
nanobot agent -m "What is 2+2?"
```

Interactive:

```bash
nanobot agent
```

You can also run via module entrypoint:

```bash
python -m nanobot agent -m "hello"
```

### Gateway (chat apps / channels)

Start the gateway:

```bash
nanobot gateway
```

The gateway is what connects nanobot to chat “channels” (Telegram/Discord/WhatsApp/Feishu). If you want to communicate with nanobot via Discord, you generally **need `nanobot gateway` running**.

Then enable/configure channels in `~/.nanobot/config.json`, as described in `README.md`.

#### Discord quickstart (minimal config)

1) Put your Discord bot token in:

- `channels.discord.token` (this is the **Discord bot token** from the Discord Developer Portal)

2) Enable the channel:

- `channels.discord.enabled: true`

3) (Recommended) Restrict who can talk to the bot:

- `channels.discord.allowFrom: ["YOUR_USER_ID"]`
  - `allowFrom` is an **allow-list (whitelist)** of Discord user IDs
  - `[]` (empty) means **allow everyone**

Example:

```json
{
  "channels": {
    "discord": {
      "enabled": true,
      "token": "YOUR_DISCORD_BOT_TOKEN",
      "allowFrom": ["YOUR_USER_ID"]
    }
  }
}
```

Also ensure you have at least one LLM provider API key configured (otherwise the gateway will exit with “No API key configured”).

#### Sanity checks

```bash
nanobot channels status
nanobot status
```

## WhatsApp development notes (bridge)

WhatsApp support uses the Node/TypeScript bridge in `bridge/`, and the Python runtime connects to it over WebSocket (default `ws://localhost:3001`).

### Link your device (QR)

In one terminal:

```bash
nanobot channels login
```

This will:

- Copy the bridge into `~/.nanobot/bridge/` (if needed)
- Run `npm install` + `npm run build` there (if needed)
- Start the bridge (`npm start`) and show the QR code

In a second terminal, run:

```bash
nanobot gateway
```

If you change `bridge/` source code and want to test it, re-run `nanobot channels login` to rebuild/restart the bridge.

## Tests and lint

From the repo root (with your venv active):

```bash
pytest
ruff check .
```

## Common errors

- **“No API key configured”**
  - Add a provider key in `~/.nanobot/config.json` (for example `providers.openrouter.apiKey`), and ensure `agents.defaults.model` matches a configured provider.
- **Web search doesn’t work**
  - Set `tools.web.search.apiKey` (Brave Search API key) in `~/.nanobot/config.json` (optional feature).

