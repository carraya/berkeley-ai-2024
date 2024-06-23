from typing import List, Optional, Dict, Any
from fastapi import FastAPI
from fastapi.responses import JSONResponse
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
import logging
from firebase_admin import credentials
from aws_lambda_powertools import Logger

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

dotenv.load_dotenv(".env.example")

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()
default_app = firebase_admin.initialize_app(credential=credentials.Certificate({
    "type": "service_account",
    "project_id": "berkeley2024-d8b6a",
    "private_key_id": "fb6491fdb8437a5b14a82448d34cf8e14b40452c",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCrPkySh9E7ZBvw\nV7RAinZHz9w8tSHQxKEfJltojPeTsz+qPyh2f9rV2a15Yuoxy/8T5CdfZ3NCJPXq\n65NOi0zvRgzXxrxooepw9SkiXNxhwZm3a+44+Y29CH6LE4s9AXQaXCCy0ZOHUHw/\nIEUstT4tJYVp+PuS4OtfQyS6Te4+wHsJZDnOqi0yrHUD6S+uQzUrAsgR6JFg0iwm\nl5LBSGxBaj+LtdJAqmPtP/kfvCyc4h0WD5gZvtfhFn5P97L2lrBL88xsOdhWcEi6\n9aBc1avyqR48aHuREli+ecC6HbEAtVKs2xOn42r1PGHMUjswc4WJmAggC1fcKomG\n4AjLOzn/AgMBAAECggEADtlG5OkOBZGRGQgh3MhxqGYOLN1v/AOKc4I59UwaWh5c\nhbPjgeyYQM7jsfdK/Q85V4CcwWZEO+Oq+oUVSUxFWyiLciWmrlP/JjuIwGGlyOKm\nvgO7EzzgdrHHEOKcjw+sATuLDxzV9BFqLkPrSHMqDw25dQ6Rkfm0e/z9SrWTOrGf\nNFtOcTXkfpm4WxwxG30nrh0nCn4rKDa9P11bgJXubMSBEYp7Gg9yl+3SISTp1llq\nMDSCaFQxtEhPF3uepUrbkEm68kUfLzip4nCuDTRQ2CkF/eRm9sFjIUTVfB9e+B7T\nspCPVrSHdar6RbwfNNK/WUy6g1FSBcL9ByAQHSUqUQKBgQDl70bMwHA8cA1vsJDP\nC9FsxtrAPpilgQSRlNzNAcZ5IWt9k6k6FLrnpDoDXA1XqJDthACbPkmgRIe87co0\nYdRxFbrVIcYUsiFPnC3TuAMW90SQ1JoGSKnhxvrx3CgdnuicKyQN9kso7KHvIETH\nEQsv3yt5fa0sC8NMW/KZYelIewKBgQC+p8usK/9D0zByigJTWcdk0EVHJKacI8Iv\nkOjTpL0LIZfSJfJUUpkgKaar4Lyy0rDYEWfLkqIC/eWwzBAin6WTYeEHwqx+2MT8\nVP47RPq+qD1fIHNLyU1eblWLxjB3tZSb62woDbceGCJevyc7m5ABXo8y3CUreh4Q\nJn/phxo3TQKBgCJ3m8VVk317zofPj+V5gAsuQ9xNhdRJYsXv6qlQes/tko9gcx2h\nveK7W3bldZqOSitQfkbHL4I2w6IugwEXKSFKgJcyWN8BVLz6TGRQUSZAKqcLN4t5\nmP2fNj7LIbhO+c9vKBhvsxSPZDbUP3sXsvWaHoo3rJ3NpZjsr5EOfEnBAoGBAI+y\nQlUzGAMTwrkhgZ021o0KWJzFZ/nZDbvyGTmjOYSRPi96wEmDs7vFCMUU7sRM/lLr\n03Jgw1FD8gGt3B9sekw6AnRp6r70PIv+t1sOo3pdrVvsRloBkBmzSTC/ILqpFifq\naatKoxDAme8VXcmUdxZBIebwe+dn9A6yJchqNn0lAoGBANjzw+K+yG/w+xlFotSO\nbionM8T7GSR23qWS6Cf5SgZ0KjEGgMAQJVOjvbUMIxSSHzrHfEcqFc0zDM8Z5/6I\nJ/d3wX4tfnPJ3dRDz5tsjHFkQVZCH2c3+vyTVD3c8awGHJ8Ho259Yl/t9LPt8iT3\nw1mp/Ym2Lt/n+CkeZAi8CbYi\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-ez7q3@berkeley2024-d8b6a.iam.gserviceaccount.com",
    "client_id": "102753575769000730480",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": r"https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-ez7q3%40berkeley2024-d8b6a.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}))
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



import time
from threading import Lock

last_call_time = 0
lock = Lock()


@app.post("/save")
def save_to_firebase(string):
    doc_ref = db.collection('idk').document(string)
    
    doc_ref.set({"string": string})
    return JSONResponse(status_code=200, content={"message": "Situation added successfully"})

@app.post("/info")
def case_info(call_info: WebhookPayload):
    global last_call_time
    call_id = call_info.message.call.id
    logger.info("WE'RE IN")
                         
    with lock:
        current_time = time.time()
        if isinstance(last_call_time, int):
            last_call_time = {}
        if call_id in last_call_time and current_time - last_call_time[call_id] < 1:
            return {"message": "Too many requests. Please try again later."}
        last_call_time[call_id] = current_time

    if call_info.message.type == "transcript":
        messages = call_info.message.artifact.messagesOpenAIFormatted
        conversation = ""
        for message in messages:
            role = message.role
            content = message.content
            if content:
                conversation += f"{role}: {content}\n"
        logger.info(conversation)
   
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"Extract situation details/information from the following 911 operator transcript and provide it in JSON format. IF THE INFORMATION IS NOT GIVEN, DO NOT ATTEMPT TO FILL THAT ATTRIBUTE IN THE JSON. RETURN NONE IF NO VALUABLE INFORMATION CAN BE EXTRACTED. QUOTE THE USER FOR EACH PIECE OF INFORMATION YOU RECORD IN THE FOLLOWING STRUCUTRE: {{'location': {{'source': '<user quote>', 'info': '<extracted information>'}}}}:\n\n{conversation}"}],
            response_format={ "type": "json_object" }
        )
        logger.info(response)
       
        doc_ref = db.collection('calls').document(call_id)
        res = response.choices[0].message.content
        res_json = json.loads(res)
        
        doc_ref.set({"situation": res_json})
        return JSONResponse(status_code=200, content={"message": "Situation added successfully"})
    
handler = Mangum(app=app, lifespan="off")
