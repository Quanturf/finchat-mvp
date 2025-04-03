import json
from openai import OpenAI
from typing import Optional, List, Dict, Any
from ..constants.prompts import TOOL_SELECTION_PROMPT
from ..dataVendors.functionToolSchema import AVAILABLE_TOOLS

client = OpenAI(
    api_key="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",
    base_url="https://api.groq.com/openai/v1",
)


class LLM:
    def __init__(self):
        self.client = client

    def chatCompletion(
        self,
        model: str,
        messages: List[Dict[str, str]],
        response_format: Optional[Dict] = None,
        tools: Optional[List[Dict]] = None,
    ) -> Any:
        """
        Generates a chat completion using the specified model and parameters.

        Args:
            model: The model to use (e.g., "mixtral-8x7b-32768").
            messages: A list of message dictionaries (role, content).
            response_format: Optional response format specification.
            tools: Optional list of tools to use.

        Returns:
            The chat completion response object.
        """
        completion = self.client.chat.completions.create(
            model=model,
            messages=messages,
            response_format=response_format,
            max_tokens=2048,
            temperature=0.3,
            tools=tools,
        )

        return completion

    def select_tools(self, user_query: str) -> List[Dict[str, Any]]:
        """Selects tools and parameters based on the user's query."""

        messages = [
            {
                "role": "system",
                "content": TOOL_SELECTION_PROMPT.format(tools=AVAILABLE_TOOLS),
            },
            {"role": "user", "content": user_query},
        ]
        response = self.chatCompletion(
            model="llama-3.1-8b-instant",
            messages=messages,
            response_format={"type": "json_object"},
        )

        tool_calls = []
        response_choices = response.choices[0].message.content
        if response_choices:
            tool_calls = json.loads(response_choices)["tools"]
        return tool_calls
