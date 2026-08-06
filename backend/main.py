from fastapi import FastAPI
from pydantic import BaseModel
from.chatbot import run_chatbot
from fastapi.middleware.cors import CORSMiddleware
from typing import List,Optional,Dict
import uuid
app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    #Allow the connect with the frontend
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

session_Store:Dict[str,List[dict]]={}

class Message(BaseModel):
    message:str
    session_id:Optional[str]=None


@app.post("/chat")
def chat(data:Message):
 #  Create a new session if need
  session_id=data.session_id or str(uuid.uuid4())
 
  # history of converstation
  history=session_Store.get(session_id,[])
  #  ask chatbot
  response=run_chatbot(data.message,history)
  #  save converstaion
  history.append({
    "role":"user",
    "content":data.message
  })
  history.append({
     "role":"assistant",
     "content":response["answer"]
  })
  session_Store[session_id]=history
  return{
     "answer":response["answer"],
     "sources": response["sources"],
     "session_id":session_id
  } 
 