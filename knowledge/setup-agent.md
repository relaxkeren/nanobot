# Agent setup

How to configure nanobot’s default agent: where to set the model, provider, workspace, and sampling options.

## Config file

Nanobot reads configuration from:

- **`~/.nanobot/config.json`**

Agent behavior is controlled by:

- **`providers`** — API keys (and optional base URLs) per LLM provider
- **`agents.defaults`** — default model, workspace, and sampling/limits

## Agent defaults (`agents.defaults`)

| Option | Description | Default |
|--------|-------------|---------|
| `workspace` | Workspace directory for tool access | `~/.nanobot/workspace` |
| `model` | Model identifier; determines which provider is used | (none) |
| `maxTokens` | Maximum tokens in the model response | 8192 |
| `temperature` | Sampling temperature (0–2) | 0.7 |
| `maxToolIterations` | Max tool-call loop iterations | 20 |

Example with all defaults set:

```json
{
  "agents": {
    "defaults": {
      "workspace": "~/.nanobot/workspace",
      "model": "anthropic/claude-opus-4-5",
      "maxTokens": 8192,
      "temperature": 0.7,
      "maxToolIterations": 20
    }
  }
}
```

## How the provider is chosen

Nanobot uses **`agents.defaults.model`** to:

- Pick an API key by matching keywords in the model string: `openai`, `anthropic`, `gemini`, `qwen`, `kimi`, `moonshot`, `deepseek`, `groq`, etc.
- Optionally pick a base URL for OpenRouter, Moonshot, Zhipu, or vLLM (see provider notes below).

If no provider matches the model name, nanobot falls back to the **first non-empty API key** in `providers`. To use a specific provider, set `model` to a value that contains that provider’s keyword (e.g. `kimi-k2.5` for Moonshot, `anthropic/claude-opus-4-5` for Anthropic).

## Provider examples

Configure one or more providers under `providers`, then set `agents.defaults.model` to a model ID that matches the provider you want to use.

### Moonshot / Kimi (use Moonshot instead of Anthropic)

To use Moonshot only (no Anthropic), add a `moonshot` provider and set the default model to a Moonshot/Kimi model:

```json
{
  "providers": {
    "moonshot": {
      "apiKey": "YOUR_MOONSHOT_API_KEY"
    }
  },
  "agents": {
    "defaults": {
      "workspace": "~/.nanobot/workspace",
      "model": "kimi-k2.5",
      "maxTokens": 8192,
      "temperature": 0.7,
      "maxToolIterations": 20
    }
  }
}
```

Notes:

- The model name must contain `moonshot` or `kimi` so nanobot selects the Moonshot provider.
- Moonshot API base defaults to `https://api.moonshot.cn/v1` unless you set `providers.moonshot.apiBase`.
- For `kimi-k2.5`, temperature is forced to `1.0` by nanobot.

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

### OpenRouter

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

OpenRouter base URL defaults to `https://openrouter.ai/api/v1` if not set.

### OpenAI

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

### Groq

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

### Local models (vLLM / OpenAI-compatible)

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
      "model": "vllm/meta-llama/Llama-3.1-8B-Instruct"
    }
  }
}
```

For vLLM, the model string must contain `vllm` so nanobot uses `providers.vllm.apiBase`.

## Optional: web search and safety

- **Web search**: set `tools.web.search.apiKey` (Brave Search API key) to enable web search.
- **Safety**: set `tools.restrictToWorkspace: true` to restrict tools to the workspace; use `channels.*.allowFrom` to limit who can message the bot.

## Environment variables

You can override config with env vars: prefix `NANOBOT_`, nested keys with `__`.

Examples:

- `NANOBOT_PROVIDERS__MOONSHOT__API_KEY=...`
- `NANOBOT_AGENTS__DEFAULTS__MODEL=kimi-k2.5`

## Troubleshooting

- **“No API key configured”** — Set at least one `providers.<name>.apiKey` and ensure `agents.defaults.model` matches that provider (or rely on the first-available-key fallback).
- **Requests not using your `apiBase`** — `apiBase` is only used when the chosen provider/model triggers it; see [ai-model-setup.md](ai-model-setup.md) for provider selection details.

## See also

- [ai-model-setup.md](ai-model-setup.md) — How nanobot chooses the LLM provider, LiteLLM conventions, and full provider notes.
