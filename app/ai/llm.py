import json
from openai import OpenAI
from typing import Optional, List, Dict, Any
from ..constants.prompts import TOOL_SELECTION_PROMPT
from ..dataVendors.functionToolSchema import AVAILABLE_TOOLS
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
        tool_choice: Optional[str] = "auto",
    ) -> Any:
        try:
            completion = self.client.chat.completions.create(
                model=model,
                messages=messages,
                response_format=response_format,
                max_tokens=4096,
                temperature=0.2,
                tools=tools,
                tool_choice=tool_choice,
            )
            return completion
        except Exception as e:
            logger.error(f"Error during chat completion API call: {e}")
            raise

    def select_tools(
        self, user_query: str, chat_history: List[Dict[str, str]]
    ) -> List[Dict[str, Any]]:
        formatted_tools = json.dumps(AVAILABLE_TOOLS, indent=2)
        system_prompt = TOOL_SELECTION_PROMPT.format(tools=formatted_tools)

        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(chat_history)
        messages.append({"role": "user", "content": user_query})

        logger.info(f"Messages sent for tool selection: {messages}")

        try:
            response = self.chatCompletion(
                model="llama3-groq-70b-8192-tool-use-preview",
                messages=messages,
                tools=AVAILABLE_TOOLS,
                tool_choice="auto",
            )

            tool_calls = []
            response_message = response.choices[0].message

            if response_message.tool_calls:
                logger.info(
                    f"Tool calls selected by LLM: {response_message.tool_calls}"
                )
                for tool_call in response_message.tool_calls:
                    try:
                        arguments = json.loads(tool_call.function.arguments)
                        tool_calls.append(
                            {
                                "tool_call_id": tool_call.id,
                                "name": tool_call.function.name,
                                "arguments": arguments,
                            }
                        )
                    except json.JSONDecodeError as json_err:
                        logger.error(
                            f"Failed to parse arguments for tool {tool_call.function.name}: {tool_call.function.arguments}. Error: {json_err}"
                        )
                        # Decide how to handle malformed JSON: skip, error, attempt repair?
                        # Skipping for now:
                        continue  # Skip this tool call
                    except Exception as e:
                        logger.error(
                            f"Error processing tool call {tool_call.function.name}: {e}"
                        )
                        continue  # Skip this tool call

            else:
                logger.info("No tools selected by the LLM.")

            logger.info(f"Parsed tool calls: {tool_calls}")
            return tool_calls

        except Exception as e:
            logger.error(f"Error in select_tools during API call or processing: {e}")
            # Depending on requirements, you might want to return an empty list or raise
            return []  # Return empty list on error
