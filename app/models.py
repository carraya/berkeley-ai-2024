from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional, Dict


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
    assistantId: Optional[str] = None
    webCallUrl: Optional[str] = None


class Message(BaseModel):
    role: Optional[str] = None
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
    role: Optional[str] = None
    transcriptType: Optional[str] = None
    transcript: Optional[str] = None
    # functionCall: FunctionCall
    call: Call
    artifact: Artifact
    timestamp: datetime


class WebhookPayload(BaseModel):
    message: FunctionCallMessage


class ToolCallResult(BaseModel):
    toolCallId: str
    result: str


class ToolCallResponse(BaseModel):
    results: List[ToolCallResult]

class FunctionCalling(BaseModel):
    type: str
    role: Optional[str] = None
    transcriptType: Optional[str] = None
    transcript: Optional[str] = None
    functionCall: FunctionCall
    call: Call
    artifact: Artifact
    timestamp: datetime
    
class FunctionCallingPayload(BaseModel):
    message: FunctionCalling
