from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from ..ai.llm import LLM

chatRouter = APIRouter()
llm = LLM()


class DataVendor(BaseModel):
    name: str
    api_key: Optional[str] = None


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]
    data_vendor: DataVendor


@chatRouter.post("/")
async def chat(chat_request: ChatRequest):
    try:
        # messages = [
        #     {"role": msg.role, "content": msg.content} for msg in chat_request.messages
        # ]
        messages = chat_request.messages
        data_vendor = chat_request.data_vendor
        
        # 1st call to check for required tools
        # 2nd call for final response
        
        required_tools = llm.chatCompletion()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")
