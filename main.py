from typing import Optional, Union
from fastapi import FastAPI
from models import Suspect, CallInfo
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

@app.post("/info/")
def case_info(call_info: CallInfo):
    print(call_info)
    doc_ref = db.collection('calls').document()
    print("DOC_REF",doc_ref)
    call_info_dict = call_info.model_dump()
    doc_ref.set(call_info_dict)
    return {"message": "Call info added successfully"}