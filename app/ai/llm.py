from openai import OpenAI
from typing import Optional, List, Dict


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
        messages: List,
        response_format: Optional[Dict] = None,
        tools: Optional[List] = None,
    ):
        completion = self.client.chat.completions.create(
            model=model,
            messages=messages,
            response_format=response_format,
            max_tokens=2048,
            temperature=0.3,
            tools=tools,
        )

        return completion
