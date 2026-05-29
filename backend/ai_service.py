"""
DebugMind - AI Service
Groq + LangChain integration with few-shot structured-output prompting.
"""

import os
import json
import re
import logging
from dotenv import load_dotenv

from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

logger = logging.getLogger(__name__)

# Model setup
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
MODEL_NAME   = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")

# ── Few-shot examples embedded in the system prompt ──────────────────────────
# NOTE: SYSTEM_PROMPT is a plain Python string — NOT a LangChain PromptTemplate.
# All curly braces here are literal JSON characters; use single { } throughout.
SYSTEM_PROMPT = """You are DebugMind, an expert AI code debugging assistant.
You help developers of all skill levels understand bugs and write better code.

## Your Task
Given a code snippet (and an optional error message), you will:
1. Identify every bug or issue.
2. Explain the root cause in plain English.
3. Provide a corrected, working version of the code.
4. Suggest up to 3 concrete optimizations.

## Output Format
You MUST respond with ONLY a valid JSON object — no markdown fences, no extra text.

{
  "error_summary": "<one-sentence summary of the error(s)>",
  "root_cause": "<clear explanation of WHY the bug exists>",
  "explanation": "<beginner-friendly, step-by-step walkthrough of the problem>",
  "fixed_code": "<the complete corrected code as a string>",
  "optimizations": ["<tip 1>", "<tip 2>", "<tip 3>"]
}

---

## Few-Shot Examples

### Example 1 — Python ZeroDivisionError

**User Input**
Language: Python
Error: ZeroDivisionError: division by zero
Code:
```python
def average(numbers):
    total = sum(numbers)
    return total / len(numbers)

print(average([]))
```

**Assistant Output**
{
  "error_summary": "The function crashes with ZeroDivisionError when given an empty list.",
  "root_cause": "len([]) returns 0, and dividing by 0 is mathematically undefined, so Python raises ZeroDivisionError.",
  "explanation": "When you call average([]), the list is empty. sum([]) returns 0, but len([]) also returns 0. The line `total / len(numbers)` becomes `0 / 0`, which Python cannot compute. You need to guard against an empty list before performing the division.",
  "fixed_code": "def average(numbers):\\n    if not numbers:\\n        return 0  # or raise ValueError('List must not be empty')\\n    return sum(numbers) / len(numbers)\\n\\nprint(average([]))  # Output: 0",
  "optimizations": [
    "Raise a ValueError with a descriptive message instead of silently returning 0, so callers know the input was invalid.",
    "Use type hints (def average(numbers: list[float]) -> float) for clarity.",
    "Consider using statistics.mean() from the standard library for production code."
  ]
}

---

### Example 2 — JavaScript undefined variable

**User Input**
Language: JavaScript
Error: ReferenceError: userName is not defined
Code:
```javascript
function greetUser() {
  console.log("Hello, " + userName);
}
greetUser();
```

**Assistant Output**
{
  "error_summary": "The variable `userName` is used inside the function but was never declared or passed in.",
  "root_cause": "`userName` is referenced without being defined anywhere in scope, causing a ReferenceError at runtime.",
  "explanation": "JavaScript looks up the scope chain for `userName` and cannot find it — it was never declared with `let`, `const`, or `var`, and it was not passed as a parameter. The fix is to either pass the name as a parameter or declare it before calling the function.",
  "fixed_code": "function greetUser(userName) {\\n  console.log('Hello, ' + userName);\\n}\\ngreetUser('Alice');  // Output: Hello, Alice",
  "optimizations": [
    "Use template literals for cleaner string formatting: `Hello, ${userName}`.",
    "Add a default parameter value: function greetUser(userName = 'Guest') to handle missing arguments gracefully.",
    "Use strict mode ('use strict';) at the top of your files to catch undeclared variables earlier."
  ]
}

---

Now debug the following code provided by the user. Remember: respond with ONLY the JSON object, no markdown fences.
"""

# ── User-turn prompt template ─────────────────────────────────────────────────
USER_TEMPLATE = """Language: {language}
Error message: {error_msg}
Code:
```
{code}
```"""

prompt_template = PromptTemplate(
    input_variables=["language", "error_msg", "code"],
    template=USER_TEMPLATE,
)


def _build_llm() -> ChatGroq:
    """Instantiate the Groq LLM via LangChain."""
    if not GROQ_API_KEY:
        raise EnvironmentError(
            "GROQ_API_KEY is not set. Add it to backend/.env"
        )
    return ChatGroq(
        api_key=GROQ_API_KEY,
        model=MODEL_NAME,
        temperature=0.2,
        max_tokens=2048,
    )


def _extract_json(raw: str) -> dict:
    """
    Robustly pull the first JSON object from the model response.
    Handles cases where the model wraps JSON in markdown code fences.
    """
    # Strip markdown fences if present
    cleaned = re.sub(r"```(?:json)?", "", raw).strip()
    cleaned = cleaned.rstrip("`").strip()

    # Try direct parse first
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    # Fall back: find the first { ... } block
    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass

    raise ValueError(f"Could not parse JSON from model output:\n{raw[:500]}")


def debug_code(code: str, error_msg: str, language: str) -> dict:
    """
    Core function: sends the debugging request to Groq and returns a
    structured dict with keys: error_summary, root_cause, explanation,
    fixed_code, optimizations.
    """
    try:
        llm = _build_llm()

        # Build the user-turn message from the template
        user_message = prompt_template.format(
            language=language,
            error_msg=error_msg if error_msg else "No error message provided.",
            code=code,
        )

        # Construct messages list (system + user)
        from langchain_core.messages import SystemMessage, HumanMessage

        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=user_message),
        ]

        logger.info("Sending request to Groq model: %s", MODEL_NAME)
        response = llm.invoke(messages)
        raw_output = response.content

        logger.info("Raw model output received (%d chars)", len(raw_output))

        result = _extract_json(raw_output)

        # Validate required keys
        required_keys = {"error_summary", "root_cause", "explanation", "fixed_code", "optimizations"}
        missing = required_keys - result.keys()
        if missing:
            logger.warning("Model response missing keys: %s", missing)
            for key in missing:
                result[key] = "Not provided." if key != "optimizations" else []

        # Ensure optimizations is always a list
        if not isinstance(result.get("optimizations"), list):
            result["optimizations"] = [str(result["optimizations"])]

        return result

    except EnvironmentError as exc:
        return {"error": str(exc)}
    except ValueError as exc:
        return {"error": f"Failed to parse AI response. {exc}"}
    except Exception as exc:
        logger.exception("Unexpected error in debug_code")
        return {"error": f"An unexpected error occurred: {exc}"}