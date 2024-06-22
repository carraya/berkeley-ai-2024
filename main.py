from typing import List, Optional, Dict, Any
from fastapi import FastAPI
from models import Suspect, CallInfo
from pydantic import BaseModel
from datetime import datetime
import firebase_admin
import dotenv
from firebase_admin import firestore

dotenv.load_dotenv()

app = FastAPI()
default_app = firebase_admin.initialize_app()
db = firestore.client()


print("Current App Name:", default_app.project_id)


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
def case_info(call_info: WebhookPayload):
    print(call_info)
    doc_ref = db.collection('calls').document()
    print("DOC_REF", doc_ref)
    call_info_dict = call_info.model_dump()
    doc_ref.set(call_info_dict)
    return {"message": "Call info added successfully"}
