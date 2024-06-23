from threading import Lock
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, Request
from models import Suspect, CallInfo
from pydantic import BaseModel
from datetime import datetime
import firebase_admin
import dotenv
from firebase_admin import firestore
import openai
import os
import json
from mangum import Mangum
import time


dotenv.load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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


last_call_time = 0
lock = Lock()


@app.post("/info/")
def case_info(call_info: WebhookPayload):
    global last_call_time
    call_id = call_info.message.call.id
    # with lock:
    #     current_time = time.time()
    #     if isinstance(last_call_time, int):
    #         last_call_time = {}
    #     if call_id in last_call_time and current_time - last_call_time[call_id] < 1:
    #         return {"message": "Too many requests. Please try again later."}
    #     last_call_time[call_id] = current_time

    doc_ref = db.collection('calls').document(call_id)

    if call_info.message.type == "end-of-call-report":
        print("END OF CALL")
        try:
            # Try to update the document
            doc_ref.update({'callStatus': 'ended'})
        except:
            # If the document doesn't exist, create it
            doc_ref.set(
                {'callStatus': 'ended', 'createdDate': int(time.time())})
        return {"message": "Call status updated to ended"}

    if call_info.message.type == "conversation-update":
        print("yo")
        messages = call_info.message.artifact.messagesOpenAIFormatted
        conversation = ""
        for message in messages:
            role = message.role
            content = message.content
            if content:
                conversation += f"{role}: {content}\n"
        print("THE CONVERSATION", conversation)

        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"Extract situation details/information from the following 911 operator transcript and provide it in JSON format. IF THE INFORMATION IS NOT GIVEN, DO NOT ATTEMPT TO FILL THAT ATTRIBUTE IN THE JSON. RETURN NONE/NULL IF NO VALUABLE INFORMATION CAN BE EXTRACTED. QUOTE THE USER FOR EACH PIECE OF INFORMATION YOU RECORD IN THE FOLLOWING STRUCUTRE: {{'location': {{'source': '<user quote>', 'info': '<extracted information>'}}}}:\n\n{conversation}"}],
            response_format={"type": "json_object"}
        )
        print(response)

        res = response.choices[0].message.content
        res_json = json.loads(res)

        # Get the current document data
        doc = doc_ref.get()
        if doc.exists:
            current_data = doc.to_dict()
        else:
            current_data = {}

        # Add createdDate if it doesn't exist
        if 'createdDate' not in current_data:
            current_data['createdDate'] = int(time.time())

        # Set callStatus to "active" if it doesn't exist
        if 'callStatus' not in current_data:
            current_data['callStatus'] = 'active'

        # Update the situation field
        current_data['situation'] = res_json

        # Set the updated data back to Firestore
        doc_ref.set(current_data)

        return {"message": "Situation added successfully"}

    # if call_info.message.type == "transcript":
        # messages = call_info.message.artifact.messagesOpenAIFormatted
        # conversation = ""
        # for message in messages:
        #     role = message.role
        #     content = message.content
        #     if content:
        #         conversation += f"{role}: {content}\n"
        # print(conversation)

        # response = openai.chat.completions.create(
        #     model="gpt-3.5-turbo",
        #     messages=[{"role": "user", "content": f"Extract situation details/information from the following 911 operator transcript and provide it in JSON format. IF THE INFORMATION IS NOT GIVEN, DO NOT ATTEMPT TO FILL THAT ATTRIBUTE IN THE JSON. RETURN NONE IF NO VALUABLE INFORMATION CAN BE EXTRACTED. QUOTE THE USER FOR EACH PIECE OF INFORMATION YOU RECORD IN THE FOLLOWING STRUCUTRE: {{'location': {{'source': '<user quote>', 'info': '<extracted information>'}}}}:\n\n{conversation}"}],
        #     response_format={"type": "json_object"}
        # )
        # print(response)

        # res = response.choices[0].message.content
        # res_json = json.loads(res)

        # # Get the current document data
        # doc = doc_ref.get()
        # if doc.exists:
        #     current_data = doc.to_dict()
        # else:
        #     current_data = {}

        # # Add createdDate if it doesn't exist
        # if 'createdDate' not in current_data:
        #     current_data['createdDate'] = int(time.time())

        # # Set callStatus to "active" if it doesn't exist
        # if 'callStatus' not in current_data:
        #     current_data['callStatus'] = 'active'

        # # Update the situation field
        # current_data['situation'] = res_json

        # # Set the updated data back to Firestore
        # doc_ref.set(current_data)

        # return {"message": "Situation added successfully"}


handler = Mangum(app=app)


class ToolCallResult(BaseModel):
    toolCallId: str
    result: str


class ToolCallResponse(BaseModel):
    results: List[ToolCallResult]


@app.post("/tool/")
async def handle_tool_call(request: Request):
    data = await request.json()
    tool_call_id = data.get('toolCallId')

    # Process the tool call and get the result
    emergency_info = get_emergency_info(data)

    # Prepare the response with both the result and additional context
    result_data = {
        "emergency_type": emergency_info["type"],
        "location": emergency_info["location"],
        "severity": emergency_info["severity"],
        "nearest_unit": emergency_info["nearest_unit"],
        "instructions": emergency_info["instructions"],
        "additional_context": (
            f"This is a {emergency_info['severity']} {
                emergency_info['type']} emergency. "
            f"The nearest response unit is {
                emergency_info['nearest_unit']} minutes away. "
            f"Key instructions for this type of emergency are: {
                emergency_info['instructions']}."
        )
    }

    response = ToolCallResponse(
        results=[
            ToolCallResult(
                toolCallId=tool_call_id,
                result=json.dumps(result_data)  # Convert to JSON string
            )
        ]
    )

    return response.dict()


def get_emergency_info(data):
    # This would be replaced with actual logic to fetch emergency information
    return {
        "type": "fire",
        "location": "Downtown, Main St and 5th Ave",
        "severity": "high",
        "nearest_unit": "5",
        "instructions": "1. Stay low to avoid smoke. 2. Use stairs, not elevators. 3. Feel doors for heat before opening."
    }