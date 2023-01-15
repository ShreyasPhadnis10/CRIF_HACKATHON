#RODO: Use FASTAPI or something like that

from fastapi import FastAPI
from fastapi import Response, Request
from fastapi.middleware.cors import CORSMiddleware
from Selenium_test import get_company_articles
import firebase_admin
from firebase_admin import credentials

if not firebase_admin._apps:
    cred = credentials.Certificate('cirfproject-firebase-adminsdk-o9myp-0daa4e01f4.json') 
    default_app = firebase_admin.initialize_app(cred)

from firebase_admin import firestore


import json

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




l2 = []
@app.get("/articles")
async def run_company_articles (name):
   
   data = []
   data =  get_company_articles(name)
   # json_data = json.dumps(data)
   
   
   return data

@app.get("/risk_entities")
async def get_risk_entities (name):
      
      db = firestore.client()
      doc_ref = db.collection("risk_entities").document(name)
      doc = doc_ref.get()
      return(doc.to_dict())

   

   

# @app.get("/negative")
# async def get_negative_words ():
#     return l2
