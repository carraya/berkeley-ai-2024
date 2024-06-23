import threading
from fastapi import FastAPI, HTTPException, Request
from models import WebhookPayload, ToolCallResponse, ToolCallResult, FunctionCallingPayload
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
logger.info(f"--------------------------------------------------ALL ENV {os.environ}--------------------------------------------------")
app = FastAPI()
default_app = firebase_admin.initialize_app(credential=credentials.Certificate({
    "type": "service_account",
    "project_id": "berkeley2024-d8b6a",
    "private_key_id": os.getenv("PRIVATE_KEY_ID"),
    "private_key": os.getenv("PRIVATE_KEY").replace("*n*", "\n"),
    "client_email": os.getenv("CLIENT_EMAIL"),
    "client_id": os.getenv("CLIENT_ID"),
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": os.getenv("CLIENT_CERT_URL"),
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
                
            if 'location' in current_data:
                triage_prompt = f"""
                You are a 911 operator in Los Angeles, handling behavioral health crisis calls. Use the following decision matrix to determine the appropriate response for each caller:

                **Risk Levels and Corresponding Responses:**

                1. **No Crisis/Resolved (Level 1)**
                    - **Criteria:** Caller needs support/services but not in immediate risk.
                    - **Response:** No field response required. Transfer to DMH access call center for priority line and potential peer access network referral. May request peer-response organization to assist in the "navigator" role.
                    
                2. **Immediate Risk (Level 2)**
                    - **Criteria:** Caller is in crisis but can accept immediate remote help. Includes suicidal subjects not posing an immediate threat to others.
                    - **Response:** No field response unless call assessment level changes. Live transfer to Didi Hirsch Suicide Prevention Center.

                3. **Moderate Risk (Level 3)**
                    - **Criteria:** Caller needs help in person. The public is not in immediate danger, but field response is necessary. The caller may be a danger to self, others, or gravely disabled.
                    - **Response:** Dispatch DMH psychiatric mobile response team (PMRT) or DMH van or other psych evaluation team (PET). DMH access call center will dispatch non-law enforcement team.

                4. **Higher Risk (Level 4)**
                    - **Criteria:** Immediate threat to public safety or crime. The caller or someone else is in immediate danger besides a lone suicidal subject. The subject is threatening others' personal safety/property, observed with or known access to a dangerous weapon, or reported crime requiring some level of investigation.
                    - **Response:** Dispatch patrol (B&W) units and/or Smart/MET co-response team. Future 988 linkage to 911 system for transfer if needed.

                ---

                **Conversation:**

                {conversation}

                ---

                Based on the details provided by the caller, determine whether to dispatch police, fire, and/or ambulance units. The JSON output structure should be {{'police': <boolean>, 'fire': <boolean>, 'ambulance': <boolean>}}.
                """
                
                triage_res = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": triage_prompt}],
                    response_format={"type": "json_object"}
                )
                
                dis_info = json.loads(triage_res.choices[0].message.content)
                current_data["dispatchInformation"] = dis_info
                

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


@app.post("/dispatch")
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


import requests
SERP_API_KEY = "efb7ab91a902926c12b290ef01a5c2b66f8cc08e5270d0f60079866313bec533"


def get_address_serp(location: str):
    url = 'https://serpapi.com/search?engine=google_maps'

    params = {
        "engine": "google_maps",
        "type": "search",
        "google_domain": "google.com",
        "q": location,
        "hl": "en",
        "api_key": SERP_API_KEY
    }

    try:
        # Send GET request
        response = requests.get(url, params=params)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()  # Convert response to JSON format

            print(json.dumps(data, indent=4))
            return data
        else:
            print(
                f"Request failed with status code {response.status_code} {response.json()}"
            )

    except requests.RequestException as e:
        print(f"Request failed: {e}")

    # search = GoogleSearch(params)
    # results = search.get_dict()
    

# data["local_results"][0]["address"]

@app.post("/address")
def get_address(address: FunctionCallingPayload):
    call_id = address.message.call.id
    with lock_dict_lock:
        if call_id not in call_locks:
            call_locks[call_id] = threading.Lock()
    with call_locks[call_id]:
        print("HERE AGAIN")
        if address.message.functionCall.parameters['location'] != '':
            call_id = address.message.call.id
            print("CALL_ID=====",call_id)
            doc_ref = db.collection('calls').document(call_id)
            doc = doc_ref.get()
            if doc.exists:
                current_data = doc.to_dict()
                structured_address = get_address_serp(address.message.functionCall.parameters['location'])
                if "place_results" in structured_address:
                    current_data['location'] = structured_address["place_results"]["address"]
                elif "local_results" in structured_address:
                    current_data['location'] = structured_address["local_results"][0]["address"]
                else:
                    current_data['location'] = "Unable to find address"
                print("CURRENT_DATA=====",current_data)
                doc_ref.set(current_data)
                tool_call_id = address.message.call.id
                response = ToolCallResponse(
                    results=[
                        ToolCallResult(
                            toolCallId=tool_call_id,
                            result=current_data['location']
                        )
                    ]
                )
                return response.dict()
            else:
                tool_call_id = address.message.call.id
                response = ToolCallResponse(
                    results=[
                        ToolCallResult(
                            toolCallId=tool_call_id,
                            result="No location retrieved"
                        )
                    ]
                )
                return response.dict()
            
handler = Mangum(app=app, lifespan="off")
            