import threading
from fastapi import FastAPI, HTTPException
from models import WebhookPayload, ToolCallResponse, ToolCallResult
import firebase_admin
import dotenv
from firebase_admin import firestore
import openai
import os
import json
from mangum import Mangum
import logging
from firebase_admin import credentials
import time

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


# Dictionary to store locks for each call_id
call_locks = {}
lock_dict_lock = threading.Lock()


ICON_LIST = ["FireHydrant", "Firetruck", "Flame", "Car", "Plane",
             "User", "Users", "Old", "ClipboardHeart", "Vaccine"]


def get_summary_and_icon(conversation: str, dispatch_info: str):
    # Get short summary
    summary_prompt = f"""
    Summarize the following emergency situation in 3-4 words.
    Respond ONLY with the summary, nothing else.

    Emergency details:
    Dispatch Information: {dispatch_info}
    Conversation Transcript: {conversation}

    3-4 word summary:
    """

    summary_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": summary_prompt}],
        max_tokens=20,  # Limiting to ensure a short response
        temperature=0.3  # Lower temperature for more focused output
    )
    short_summary = summary_response.choices[0].message.content.strip()

    # Get icon
    icon_prompt = f"""
    Select the most appropriate icon for this emergency situation from the list below.
    Respond ONLY with the icon name, nothing else. Make sure it keeps exact case and spelling.

    Emergency details:
    Dispatch Information: {dispatch_info}
    Conversation Transcript: {conversation}

    Icon options: {ICON_LIST}

    Selected icon:
    """

    icon_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": icon_prompt}],
        max_tokens=20,  # Limiting to ensure a single icon
        temperature=0.3  # Lower temperature for more focused output
    )
    selected_icon = icon_response.choices[0].message.content.strip()

    return short_summary, selected_icon


@app.post("/info")
def case_info(call_info: WebhookPayload):
    call_id = call_info.message.call.id

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

            doc = doc_ref.get()
            if doc.exists:
                current_data = doc.to_dict()
                existing_situation = current_data.get('situation', {})
            else:
                current_data = {}
                existing_situation = {}

            if 'createdDate' not in current_data:
                current_data['createdDate'] = int(time.time())

            if 'callStatus' not in current_data:
                current_data['callStatus'] = 'active'

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
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    response_format={"type": "json_object"}
                )

                res = response.choices[0].message.content
                new_info = json.loads(res)

                for key, value in new_info.items():
                    if key not in existing_situation or existing_situation[key] != value:
                        existing_situation[key] = value

                current_data['situation'] = existing_situation

                # Get summary and icon
                dispatch_info = current_data.get(
                    'dispatchInformation', 'No dispatch information available.')
                short_summary, selected_icon = get_summary_and_icon(
                    conversation, dispatch_info)

                current_data['shortSummary'] = short_summary
                current_data['icon'] = selected_icon

                doc_ref.set(current_data)

                return {"message": f"Situation updated successfully for call {call_id}"}
            except Exception as e:
                print(f"Error processing call {call_id}: {str(e)}")
                raise HTTPException(
                    status_code=500, detail=f"Error processing request: {str(e)}")

    return {"message": "Request processed"}


@app.post("/dispatch/")
async def handle_dispatch(call_info: WebhookPayload):
    tool_call_id = call_info.message.call.id

    doc_ref = db.collection("calls").document(tool_call_id)
    doc = doc_ref.get()

    dispatch_information = None
    if doc.exists:
        call_data = doc.to_dict()
        dispatch_information = call_data.get(
            'dispatchInformation', "We need to gather more information to dispatch help.")

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

handler = Mangum(app=app)
