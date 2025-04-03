from datetime import datetime
from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import json
import logging

from ..ai.llm import LLM
from ..dataVendors import functionTool

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

chatRouter = APIRouter()
llm = LLM()


class DataVendor(BaseModel):
    name: str
    api_key: Optional[str] = None


class Message(BaseModel):
    role: str
    content: Optional[str] = None
    tool_calls: Optional[List[Dict]] = None
    tool_call_id: Optional[str] = None
    name: Optional[str] = None


class ChatRequest(BaseModel):
    messages: List[Message]
    data_vendor: DataVendor


class ToolCallResponseItem(BaseModel):
    tool_call_id: str
    name: str
    arguments: Dict[str, Any]


class ToolSelectionResponse(BaseModel):
    tools: List[ToolCallResponseItem]


class ChatResponse(BaseModel):
    response: str
    tool_calls: Optional[List[Dict]] = None


@chatRouter.post("/select-tools", response_model=ToolSelectionResponse)
async def route_select_tools(chat_request: ChatRequest):
    try:
        user_query = chat_request.messages[-1].content
        if not user_query:
            raise HTTPException(status_code=400, detail="User query cannot be empty.")

        chat_history = [
            msg.model_dump(exclude_none=True) for msg in chat_request.messages[:-1]
        ]
        selected_tools = llm.select_tools(user_query, chat_history)

        tools_to_return = [
            ToolCallResponseItem(
                tool_call_id=tool["tool_call_id"],
                name=tool["name"],
                arguments=tool["arguments"],
            )
            for tool in selected_tools
        ]
        return ToolSelectionResponse(tools=tools_to_return)

    except Exception as e:
        logger.exception(f"Error in /select-tools endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Error selecting tools: {str(e)}")


@chatRouter.post("/", response_model=ChatResponse)
async def chat(chat_request: ChatRequest):
    try:
        logger.info(
            f"Received chat request: {chat_request.model_dump(exclude_none=True)}"
        )
        current_messages = [
            msg.model_dump(exclude_none=True) for msg in chat_request.messages
        ]
        user_query = current_messages[-1].get("content")
        if not user_query:
            raise HTTPException(
                status_code=400, detail="Last message must contain user query content."
            )

        data_vendor_name = chat_request.data_vendor.name
        data_vendor_api_key = chat_request.data_vendor.api_key

        system_prompt_date = {
            "role": "system",
            "content": f"Today's date is {datetime.today().strftime('%Y-%m-%d')}. Use this for any date calculations if the user doesn't specify a range.",
        }
        if not any(
            msg.get("role") == "system" and "Today" in msg.get("content", "")
            for msg in current_messages
        ):
            current_messages.insert(0, system_prompt_date)

        first_llm_response = llm.chatCompletion(
            model="llama3-groq-70b-8192-tool-use-preview",
            messages=current_messages,
            tools=functionTool.AVAILABLE_TOOLS,
            tool_choice="auto",
        )

        response_message = first_llm_response.choices[0].message
        current_messages.append(response_message.model_dump(exclude_none=True))

        tool_calls_made = response_message.tool_calls
        function_results_for_llm = []

        if tool_calls_made:
            logger.info(
                f"LLM requested tools: {[tc.function.name for tc in tool_calls_made]}"
            )
            for tool_call in tool_calls_made:
                function_name = tool_call.function.name
                tool_call_id = tool_call.id
                try:
                    function_args = json.loads(tool_call.function.arguments)
                    logger.info(
                        f"Attempting to call tool: {function_name} with args: {function_args}"
                    )

                    function_args["data_vendor"] = data_vendor_name
                    if data_vendor_api_key:
                        function_args["api_key"] = data_vendor_api_key

                    if hasattr(functionTool, function_name):
                        function_to_call = getattr(functionTool, function_name)
                        try:
                            function_result_data = function_to_call(**function_args)
                            result_content = json.dumps(function_result_data)
                            logger.info(
                                f"Tool {function_name} executed successfully. Result chars: {len(result_content)}"
                            )
                        except Exception as func_exc:
                            logger.exception(
                                f"Error executing tool {function_name} function: {func_exc}"
                            )
                            result_content = json.dumps(
                                {
                                    "error": f"Error executing tool {function_name}: {str(func_exc)}"
                                }
                            )

                        function_results_for_llm.append(
                            {
                                "role": "tool",
                                "tool_call_id": tool_call_id,
                                "name": function_name,
                                "content": result_content,
                            }
                        )
                    else:
                        logger.warning(
                            f"Function {function_name} not found in functionTool module."
                        )
                        function_results_for_llm.append(
                            {
                                "role": "tool",
                                "tool_call_id": tool_call_id,
                                "name": function_name,
                                "content": json.dumps(
                                    {
                                        "error": f"Tool {function_name} is defined but not implemented."
                                    }
                                ),
                            }
                        )
                except json.JSONDecodeError as json_err:
                    logger.error(
                        f"Failed to parse arguments for tool {function_name}: {tool_call.function.arguments}. Error: {json_err}"
                    )
                    function_results_for_llm.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call_id,
                            "name": function_name,
                            "content": json.dumps(
                                {
                                    "error": f"Invalid arguments format received for tool {function_name}."
                                }
                            ),
                        }
                    )
                except Exception as e:
                    logger.exception(
                        f"General error processing tool call {function_name}: {e}"
                    )
                    function_results_for_llm.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call_id,
                            "name": function_name,
                            "content": json.dumps(
                                {
                                    "error": f"Server error processing tool call for {function_name}."
                                }
                            ),
                        }
                    )

            current_messages.extend(function_results_for_llm)

            logger.info("Sending tool results back to LLM for final response.")
            final_llm_response = llm.chatCompletion(
                model="llama3-groq-70b-8192-tool-use-preview", messages=current_messages
            )
            final_response_content = final_llm_response.choices[0].message.content
            logger.info(
                f"Final LLM response generated. Length: {len(final_response_content)}"
            )

        else:
            logger.info("No tools requested by LLM. Using initial response.")
            final_response_content = (
                response_message.content
                if response_message.content
                else "I received your request, but I don't have a specific action to take or information to provide based on it. Could you please provide more details or ask a different question?"
            )

        return ChatResponse(response=final_response_content)

    except HTTPException as http_exc:
        logger.error(f"HTTP Exception in chat endpoint: {http_exc.detail}")
        raise http_exc
    except Exception as e:
        logger.exception(f"Unexpected error in chat endpoint: {e}")
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {str(e)}"
        )
