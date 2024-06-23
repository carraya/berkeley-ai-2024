import threading
from fastapi import FastAPI, Request
from models import WebhookPayload, ToolCallResponse, ToolCallResult
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


@app.post("/info/")
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
