# Spec: AI Platform & LLM Gateway

- **Status**: Ready
- **Owner**: AI Platform Team (Antigravity AI Coding Agent)
- **Date**: 2026-07-04

## 1. Purpose
Define the LLM model adapters, prompt registries, structured schema output validations, and safety filtering interfaces.

## 2. Responsibilities
- Interconnect with cloud model provider APIs (Gemini, Claude, OpenAI) through isolated adapter classes.
- Parse text prompts and inject context variables from RAG or booking databases.
- Enforce output formatting by verifying LLM JSON outputs against Pydantic models.
- Track LLM latency and log input/output token metrics grouped by model and session tags.

## 3. Dependencies
- **LLM Provider SDKs** (e.g. `google-genai`, `anthropic`, `openai`).
- **Pydantic v2**: For model schema definitions and output validation.
- **Observability Platform**: For exporting token count logs and latency histories.

## 4. Public Interfaces
```python
class LlmAdapter(ABC):
    @abstractmethod
    async def generate_response(
        self, messages: List[ChatMessage], output_schema: Type[BaseModel]
    ) -> BaseModel:
        """Sends messages to LLM API and enforces validation against the schema."""
        pass

class PromptRegistry:
    def load_prompt(self, template_name: str) -> str:
        """Fetches prompt templates from disk files."""
        pass
```

## 5. Configuration
- `ACTIVE_LLM_PROVIDER`: Name of the default active model provider (e.g., `gemini`, `claude`).
- `LLM_MODEL_NAME`: specific model name (e.g. `gemini-1.5-flash`).
- `LLM_API_KEY`: Environment secret key used to authorize API calls.

## 6. Failure Modes
- **LLM Connection Errors / Timeouts**: If a call times out, retry up to 3 times with exponential backoff before failing over to a secondary provider or returning a static apology template.
- **Pydantic Validation Failures**: If LLM output fails schema validation, send a corrective prompt containing the validation error back to the LLM to auto-correct once. If that fails, log a parsing exception.

## 7. Security Considerations
- Validate LLM inputs for instruction injections.
- Exclude user passwords and tokens from prompt payloads.

## 8. Testing Strategy
- **Unit Tests**: Mock LLM responses to test validation logic, error backoffs, and prompt parameter injection.
- **Evaluation Tests**: Run structured prompts against real endpoints periodically, comparing outputs to expected test schemas.
