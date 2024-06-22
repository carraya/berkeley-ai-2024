from typing import List, Optional, Dict, Any
from fastapi import FastAPI
from models import Suspect, CallInfo
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


class FunctionCall(BaseModel):
    name: str
    parameters: Dict[str, Optional[str]] = {}


class ToolCall(BaseModel):
    id: str
    type: str
    function: FunctionCall


class Call(BaseModel):
    id: str
    orgId: str
    createdAt: datetime
    updatedAt: datetime
    type: str
    status: str
    assistantId: str
    webCallUrl: str


class Message(BaseModel):
    role: str
    message: Optional[str] = None
    time: float
    endTime: Optional[float] = None
    secondsFromStart: float
    source: Optional[str] = ""
    duration: Optional[float] = None
    toolCalls: Optional[List[ToolCall]] = None


class OpenAIFormattedMessage(BaseModel):
    role: str
    content: Optional[str] = None
    tool_calls: Optional[List[ToolCall]] = None


class Artifact(BaseModel):
    messages: List[Message]
    messagesOpenAIFormatted: List[OpenAIFormattedMessage]


class FunctionCallMessage(BaseModel):
    type: str
    functionCall: FunctionCall
    call: Call
    artifact: Artifact


class WebhookPayload(BaseModel):
    message: FunctionCallMessage


@app.post("/info/")
async def case_info(call_info: WebhookPayload):
    # print("HERE IS INFO")
    # print(call_info)
    print(call_info.message.functionCall.parameters)
    return call_info
