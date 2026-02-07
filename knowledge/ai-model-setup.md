# AI model setup (LLM providers & options)

This doc explains how nanobot chooses an LLM provider + model, and which configuration knobs affect model behavior.

> Note: nanobot uses **LiteLLM** under the hood, so model identifiers generally follow LiteLLM’s provider/model naming conventions.

## Where to configure

Nanobot reads configuration from:

- `~/.nanobot/config.json`

The two main sections for LLM setup are:

- `providers`: credentials + optional endpoints per provider
- `agents.defaults`: the default model and sampling/limits

## Core concepts

### `apiKey` vs `apiBase`

- **`providers.<name>.apiKey`**: the API key for that provider.
- **`providers.<name>.apiBase`**: the **base URL (endpoint root)** for that provider (usually `null`).

Leave `apiBase: null` unless you need a custom endpoint (proxy/gateway/self-hosted server).

### How nanobot picks which provider to use

Nanobot uses the configured `agents.defaults.model` string to:

- pick an API key (`config.get_api_key()`), by matching keywords like `openai`, `anthropic`, `gemini`, `qwen`, `kimi`, etc.
- sometimes pick a base URL (`config.get_api_base()`), currently only special-casing:
  - OpenRouter (defaults to `https://openrouter.ai/api/v1`)
  - Zhipu/GLM/Z.ai (uses `providers.zhipu.apiBase` if set)
  - vLLM (uses `providers.vllm.apiBase`, **only when the model string contains `vllm`**)

If nanobot can’t match a provider by model name, it falls back to the **first non-empty API key** in your `providers` config.

## Set the default model

Set:

- `agents.defaults.model`

Example (OpenRouter usage, but model is an Anthropic model ID):

```json
{
  "providers": {
    "openrouter": { "apiKey": "sk-or-v1-..." }
  },
  "agents": {
    "defaults": {
      "model": "anthropic/claude-opus-4-5"
    }
  }
}
```

## Provider setups (examples)

Below are common patterns. You can configure multiple providers at once and switch by changing `agents.defaults.model`.

### OpenRouter (recommended aggregator)

```json
{
  "providers": {
    "openrouter": {
      "apiKey": "sk-or-v1-..."
    }
  },
  "agents": {
    "defaults": {
      "model": "anthropic/claude-opus-4-5"
    }
  }
}
```

Notes:

- If you don’t set `providers.openrouter.apiBase`, nanobot uses `https://openrouter.ai/api/v1`.

### Anthropic (Claude direct)

```json
{
  "providers": {
    "anthropic": {
      "apiKey": "sk-ant-..."
    }
  },
  "agents": {
    "defaults": {
      "model": "anthropic/claude-opus-4-5"
    }
  }
}
```

### OpenAI (GPT direct)

```json
{
  "providers": {
    "openai": {
      "apiKey": "sk-..."
    }
  },
  "agents": {
    "defaults": {
      "model": "openai/gpt-4o-mini"
    }
  }
}
```

### DeepSeek

```json
{
  "providers": {
    "deepseek": {
      "apiKey": "sk-..."
    }
  },
  "agents": {
    "defaults": {
      "model": "deepseek/deepseek-chat"
    }
  }
}
```

### Groq (also used for Telegram voice transcription)

```json
{
  "providers": {
    "groq": {
      "apiKey": "gsk_..."
    }
  },
  "agents": {
    "defaults": {
      "model": "groq/llama-3.1-70b-versatile"
    }
  }
}
```

Notes:

- If Groq is configured, nanobot can transcribe Telegram voice/audio messages via Whisper (see `README.md`).

### Gemini

```json
{
  "providers": {
    "gemini": {
      "apiKey": "..."
    }
  },
  "agents": {
    "defaults": {
      "model": "gemini/gemini-1.5-pro"
    }
  }
}
```

### DashScope / Qwen

```json
{
  "providers": {
    "dashscope": {
      "apiKey": "..."
    }
  },
  "agents": {
    "defaults": {
      "model": "qwen-max"
    }
  }
}
```

Notes:

- nanobot will add a `dashscope/` prefix automatically for Qwen/DashScope models when needed.

### Moonshot / Kimi

```json
{
  "providers": {
    "moonshot": {
      "apiKey": "..."
    }
  },
  "agents": {
    "defaults": {
      "model": "kimi-k2.5"
    }
  }
}
```

Notes:

- nanobot sets `MOONSHOT_API_BASE` to `https://api.moonshot.cn/v1` by default (unless you provide an `apiBase`).
- `kimi-k2.5` is treated specially: temperature is forced to `1.0`.

### Zhipu / GLM / Z.ai

```json
{
  "providers": {
    "zhipu": {
      "apiKey": "..."
    }
  },
  "agents": {
    "defaults": {
      "model": "glm-4.7-flash"
    }
  }
}
```

Notes:

- If your model name contains `glm` / `zhipu` / `zai` and you don’t prefix it, nanobot will normalize it to a `zai/<model>` form internally.

### Local models (vLLM / OpenAI-compatible server)

To point nanobot at a local OpenAI-compatible server, set a provider `apiBase` to your server’s `/v1` base URL.

Example:

```json
{
  "providers": {
    "vllm": {
      "apiKey": "dummy",
      "apiBase": "http://localhost:8000/v1"
    }
  },
  "agents": {
    "defaults": {
      "model": "meta-llama/Llama-3.1-8B-Instruct"
    }
  }
}
```

Important note (current behavior):

- nanobot only returns `providers.vllm.apiBase` from `config.get_api_base()` if your `agents.defaults.model` string contains `vllm`. If you configure `providers.vllm.apiBase` but see requests still going to a default endpoint, try using a model name that includes `vllm` (or adjust your model naming so nanobot can select the vLLM base URL).

## “Other options” that affect model behavior

### Sampling and limits

Under `agents.defaults`:

- `maxTokens`: maximum tokens in the model response (default: 8192 in schema)
- `temperature`: sampling temperature (default: 0.7)
- `maxToolIterations`: max tool-call loop iterations (default: 20)
- `workspace`: workspace path (defaults to `~/.nanobot/workspace`)

Example:

```json
{
  "agents": {
    "defaults": {
      "model": "anthropic/claude-opus-4-5",
      "maxTokens": 4096,
      "temperature": 0.2,
      "maxToolIterations": 10
    }
  }
}
```

### Web search (optional)

If you want web search tool support, set:

- `tools.web.search.apiKey` (Brave Search API key)

### Safety knobs (recommended)

- `tools.restrictToWorkspace: true` to restrict tool access to the workspace directory.
- `channels.*.allowFrom` to restrict who can message your bot (empty list allows everyone).

## Troubleshooting

- **Gateway exits with “No API key configured”**
  - Set at least one `providers.<name>.apiKey`.
  - Ensure `agents.defaults.model` matches a provider you configured (or rely on the fallback “first available key” behavior).
- **You set `apiBase`, but requests aren’t going where you expect**
  - `apiBase` is only used when nanobot selects and passes it through to the provider adapter. Double-check `config.get_api_base()` behavior for your model/provider combination (not all providers use `apiBase` today).

## Environment-variable configuration (optional)

The config system supports environment variables with prefix `NANOBOT_` and nested keys separated by `__`.

Example (conceptual):

- `NANOBOT_PROVIDERS__OPENROUTER__API_KEY=...`
- `NANOBOT_AGENTS__DEFAULTS__MODEL=anthropic/claude-opus-4-5`

