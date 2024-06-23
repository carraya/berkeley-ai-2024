from threading import Lock
import threading
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


# Dictionary to store locks for each call_id
call_locks = {}
lock_dict_lock = threading.Lock()


@app.post("/info/")
def case_info(call_info: WebhookPayload):
    call_id = call_info.message.call.id

    # Acquire the lock for this specific call_id
    with lock_dict_lock:
        if call_id not in call_locks:
            call_locks[call_id] = threading.Lock()

    with call_locks[call_id]:
        doc_ref = db.collection('calls').document(call_id)

        if call_info.message.type == "end-of-call-report":
            print(f"END OF CALL: {call_id}")
            try:
                doc_ref.update({'callStatus': 'ended'})
            except:
                doc_ref.set(
                    {'callStatus': 'ended', 'createdDate': int(time.time())})
            return {"message": "Call status updated to ended"}

        if call_info.message.type == "conversation-update":
            print(f"Conversation update received for call: {call_id}")
            messages = call_info.message.artifact.messagesOpenAIFormatted
            conversation = ""
            for message in messages:
                role = message.role
                content = message.content
                if content:
                    conversation += f"{role}: {content}\n"
            print(f"THE CONVERSATION for call {call_id}:", conversation)

            # Get the current document data
            doc = doc_ref.get()
            if doc.exists:
                current_data = doc.to_dict()
                existing_situation = current_data.get('situation', {})
            else:
                current_data = {}
                existing_situation = {}

            # Add createdDate if it doesn't exist
            if 'createdDate' not in current_data:
                current_data['createdDate'] = int(time.time())

            # Set callStatus to "active" if it doesn't exist
            if 'callStatus' not in current_data:
                current_data['callStatus'] = 'active'

            # Prepare the prompt with existing situation and new conversation
            prompt = f"""
            Given the existing situation details:
            {json.dumps(existing_situation, indent=2)}

            And the following 911 operator transcript:
            {conversation}

            Extract any new or updated situation details/information and provide it in JSON format.
            If the information is not given or hasn't changed, do not include that attribute in the JSON.
            Quote the user for each piece of new or updated information you record in the following structure:
            {{'<attribute>': {{'source': '<user quote>', 'info': '<extracted information>'}}}}
            """

            try:
                response = openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    response_format={"type": "json_object"}
                )
                print(f"OpenAI response for call {call_id}:", response)

                res = response.choices[0].message.content
                new_info = json.loads(res)

                # Merge new information with existing situation
                for key, value in new_info.items():
                    if key not in existing_situation or existing_situation[key] != value:
                        existing_situation[key] = value

                # Update the situation field in the current data
                current_data['situation'] = existing_situation

                # Set the updated data back to Firestore
                doc_ref.set(current_data)

                return {"message": f"Situation updated successfully for call {call_id}"}
            except Exception as e:
                print(f"Error processing call {call_id}: {str(e)}")
                raise HTTPException(
                    status_code=500, detail=f"Error processing request: {str(e)}")

    # Clean up the lock if the call is ended
    if call_info.message.type == "end-of-call-report":
        with lock_dict_lock:
            call_locks.pop(call_id, None)

    return {"message": "Request processed"}


handler = Mangum(app=app)


class ToolCallResult(BaseModel):
    toolCallId: str
    result: str  # This should be a string, not a dict


class ToolCallResponse(BaseModel):
    results: List[ToolCallResult]


@app.post("/dispatch/")
async def handle_dispatch(call_info: WebhookPayload):
    tool_call_id = call_info.message.call.id

    doc_ref = db.collection("calls").document(tool_call_id)
    doc = doc_ref.get()

    dispatch_information = "There is no dispatch information available."
    if doc.exists:
        call_data = doc.to_dict()
        dispatch_information = call_data.get('dispatchInformation', False)

        if dispatch_information:
            dispatch_information = call_data.get('dispatchInformation', None)

    response = ToolCallResponse(
        results=[
            ToolCallResult(
                toolCallId=tool_call_id,
                result=dispatch_information
            )
        ]
    )
    # print(response)
    return response.dict()
