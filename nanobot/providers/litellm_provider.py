"""LiteLLM provider implementation for multi-provider support."""

import json
import logging
import os
import re
import uuid
from typing import Any

import litellm
from litellm import acompletion

from nanobot.providers.base import LLMProvider, LLMResponse, ToolCallRequest

logger = logging.getLogger(__name__)


def print_kwargs(kwargs: dict[str, Any]) -> None:
    """Log kwargs as key:value per line; use multi-line format when value is long or contains newline."""
    # logger.info(json.dumps(kwargs, indent=2, default=str))
    print(json.dumps(kwargs, indent=2, default=str))


def _extract_tool_calls_from_content(content: str | None) -> tuple[str, list[ToolCallRequest]]:
    """
    Fallback: when the server returns tool calls as raw text in content (e.g. Qwen3
    with a format vLLM's parser didn't recognize), extract them and strip
    thinking/tool_call blocks from the visible content.

    Looks for <tool_call>{"name": "...", "arguments": {...}}</tool_call> and
    strips <think>...</think> blocks so they are not shown to the user.
    """
    if not content or not content.strip():
        return content or "", []

    tool_calls: list[ToolCallRequest] = []
    # Match <tool_call>...</tool_call> and extract JSON (brace-balanced so nested {} work)
    tool_call_start = re.compile(r"<tool_call>\s*", re.IGNORECASE)
    clean_parts = []
    last_end = 0
    pos = 0

    while True:
        m = tool_call_start.search(content, pos)
        if not m:
            break
        start = m.end()
        # Find matching closing </tool_call>
        end_tag = content.find("</tool_call>", start)
        if end_tag == -1:
            break
        json_str = content[start:end_tag].strip()
        # Extract JSON object (brace-balanced)
        if json_str.startswith("{"):
            depth = 0
            for i, c in enumerate(json_str):
                if c == "{":
                    depth += 1
                elif c == "}":
                    depth -= 1
                    if depth == 0:
                        json_str = json_str[: i + 1]
                        break
        before = content[last_end : m.start()]
        before = re.sub(r"<think>.*?</think>", "", before, flags=re.DOTALL | re.IGNORECASE)
        before = before.strip()
        if before:
            clean_parts.append(before)
        try:
            payload = json.loads(json_str)
            name = payload.get("name") or payload.get("function", {}).get("name")
            arguments = payload.get("arguments") or payload.get("function", {}).get("arguments", "{}")
            if isinstance(arguments, str):
                arguments = json.loads(arguments) if arguments.strip() else {}
            if name:
                tool_calls.append(
                    ToolCallRequest(
                        id=str(uuid.uuid4()),
                        name=name,
                        arguments=arguments,
                    )
                )
        except (json.JSONDecodeError, TypeError) as e:
            logger.debug("Could not parse tool_call JSON from content: %s", e)
        last_end = end_tag + len("</tool_call>")
        pos = last_end

    # Remainder after last match: strip <think>
    after = content[last_end:]
    after = re.sub(r"<think>.*?</think>", "", after, flags=re.DOTALL | re.IGNORECASE)
    after = after.strip()
    if after:
        clean_parts.append(after)

    cleaned = "\n\n".join(p for p in clean_parts if p).strip()
    return cleaned, tool_calls


class LiteLLMProvider(LLMProvider):
    """
    LLM provider using LiteLLM for multi-provider support.

    Supports OpenRouter, Anthropic, OpenAI, Gemini, and many other providers through
    a unified interface.
    """
    
    def __init__(
        self, 
        api_key: str | None = None, 
        api_base: str | None = None,
        default_model: str = "anthropic/claude-opus-4-5"
    ):
        super().__init__(api_key, api_base)
        self.default_model = default_model
        
        # Detect OpenRouter by api_key prefix or explicit api_base
        self.is_openrouter = (
            (api_key and api_key.startswith("sk-or-")) or
            (api_base and "openrouter" in api_base)
        )
        
        # Only use vLLM path when model name indicates vLLM (avoid treating Moonshot/DashScope custom api_base as vLLM)
        self.is_vllm = (
            bool(api_base)
            and not self.is_openrouter
            and "vllm" in (default_model or "").lower()
        )
        
        # Configure LiteLLM based on provider
        if api_key:
            if self.is_openrouter:
                # OpenRouter mode - set key
                os.environ["OPENROUTER_API_KEY"] = api_key
            elif self.is_vllm:
                # vLLM/custom endpoint - uses OpenAI-compatible API
                os.environ["HOSTED_VLLM_API_KEY"] = api_key
            elif "deepseek" in default_model:
                os.environ.setdefault("DEEPSEEK_API_KEY", api_key)
            elif "anthropic" in default_model:
                os.environ.setdefault("ANTHROPIC_API_KEY", api_key)
            elif "openai" in default_model or "gpt" in default_model:
                os.environ.setdefault("OPENAI_API_KEY", api_key)
            elif "gemini" in default_model.lower():
                os.environ.setdefault("GEMINI_API_KEY", api_key)
            elif "zhipu" in default_model or "glm" in default_model or "zai" in default_model:
                os.environ.setdefault("ZAI_API_KEY", api_key)
            elif "dashscope" in default_model or "qwen" in default_model.lower():
                os.environ.setdefault("DASHSCOPE_API_KEY", api_key)
            elif "groq" in default_model:
                os.environ.setdefault("GROQ_API_KEY", api_key)
            elif "moonshot" in default_model or "kimi" in default_model:
                os.environ.setdefault("MOONSHOT_API_KEY", api_key)
                os.environ.setdefault("MOONSHOT_API_BASE", api_base or "https://api.moonshot.ai/v1")
        
        if api_base:
            litellm.api_base = api_base
        
        # Disable LiteLLM logging noise
        litellm.suppress_debug_info = True
    
    async def chat(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
        model: str | None = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
    ) -> LLMResponse:
        """
        Send a chat completion request via LiteLLM.
        
        Args:
            messages: List of message dicts with 'role' and 'content'.
            tools: Optional list of tool definitions in OpenAI format.
            model: Model identifier (e.g., 'anthropic/claude-sonnet-4-5').
            max_tokens: Maximum tokens in response.
            temperature: Sampling temperature.
        
        Returns:
            LLMResponse with content and/or tool calls.
        """
        model = model or self.default_model
        
        # For OpenRouter, prefix model name if not already prefixed
        if self.is_openrouter and not model.startswith("openrouter/"):
            model = f"openrouter/{model}"
        
        # For Zhipu/Z.ai, ensure prefix is present
        # Handle cases like "glm-4.7-flash" -> "zai/glm-4.7-flash"
        if ("glm" in model.lower() or "zhipu" in model.lower()) and not (
            model.startswith("zhipu/") or 
            model.startswith("zai/") or 
            model.startswith("openrouter/")
        ):
            model = f"zai/{model}"

        # For DashScope/Qwen, ensure dashscope/ prefix
        if ("qwen" in model.lower() or "dashscope" in model.lower()) and not (
            model.startswith("dashscope/") or
            model.startswith("openrouter/")
        ):
            if self.is_vllm:
                # If the config uses `vllm/<model-id>` as a hint, strip it before routing.
                if model.lower().startswith("vllm/"):
                    model = model.split("/", 1)[1]
                model = f"openai/{model}"
            else:
                model = f"dashscope/{model}"

        # For Moonshot/Kimi, ensure moonshot/ prefix (before vLLM check)
        if ("moonshot" in model.lower() or "kimi" in model.lower()) and not (
            model.startswith("moonshot/") or model.startswith("openrouter/")
        ):
            model = f"moonshot/{model}"

        # For Gemini, ensure gemini/ prefix if not already present
        if "gemini" in model.lower() and not model.startswith("gemini/"):
            model = f"gemini/{model}"


        # For vLLM, use hosted_vllm/ prefix per LiteLLM docs
        # Convert openai/ prefix to hosted_vllm/ if user specified it
        # Comment this out and replace it with local vLLM mode above
        # if self.is_vllm:
        #     model = f"hosted_vllm/{model}"
        
        # kimi-k2.5 only supports temperature=1.0
        if "kimi-k2.5" in model.lower():
            temperature = 1.0

        kwargs: dict[str, Any] = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }

        # OpenAI-compatible endpoints require a non-empty api_key; for local vLLM this can be any string.
        if self.is_vllm and self.api_key:
            kwargs["api_key"] = self.api_key

        # Pass api_base directly for custom endpoints (vLLM, etc.)
        if self.api_base:
            kwargs["api_base"] = self.api_base
        
        if tools:
            kwargs["tools"] = tools
            kwargs["tool_choice"] = "auto"
        
        try:
            print_kwargs(kwargs)
            response = await acompletion(**kwargs)
            return self._parse_response(response)
        except Exception as e:
            # Return error as content for graceful handling
            return LLMResponse(
                content=f"Error calling LLM: {str(e)}",
                finish_reason="error",
            )
    
    def _parse_response(self, response: Any) -> LLMResponse:
        """Parse LiteLLM response into our standard format."""
        choice = response.choices[0]
        message = choice.message
        
        tool_calls: list[ToolCallRequest] = []
        content = message.content or ""
        
        if hasattr(message, "tool_calls") and message.tool_calls:
            for tc in message.tool_calls:
                # Parse arguments from JSON string if needed
                args = tc.function.arguments
                if isinstance(args, str):
                    import json
                    try:
                        args = json.loads(args)
                    except json.JSONDecodeError:
                        args = {"raw": args}
                
                tool_calls.append(ToolCallRequest(
                    id=tc.id,
                    name=tc.function.name,
                    arguments=args,
                ))
        
        # Fallback: some backends (e.g. vLLM + Qwen3) return tool calls as raw text
        # in content when their parser doesn't match the model's output format.
        # To avoid changing behavior for non-vLLM providers, only enable this in vLLM mode.
        if self.is_vllm and not tool_calls and content:
            content, tool_calls = _extract_tool_calls_from_content(content)
        
        usage = {}
        if hasattr(response, "usage") and response.usage:
            usage = {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
            }
        
        # Extract reasoning content if present (common in thinking models like Moonshot)
        reasoning_content = getattr(message, "reasoning_content", None)
        if not reasoning_content and hasattr(message, "provider_specific_fields"):
             reasoning_content = message.provider_specific_fields.get("reasoning_content")

        return LLMResponse(
            content=content,
            tool_calls=tool_calls,
            finish_reason=choice.finish_reason or "stop",
            usage=usage,
            reasoning_content=reasoning_content,
        )
    
    def get_default_model(self) -> str:
        """Get the default model."""
        return self.default_model
