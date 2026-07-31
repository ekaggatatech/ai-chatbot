from fastapi import FastAPI
from pydantic import BaseModel
from.chatbot import run_chatbot
from fastapi.middleware.cors import CORSMiddleware
# from.model import ContactForm

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    #Allow the connect with the frontend
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class Message(BaseModel):
    message:str


@app.post("/chat")
def chat(data:Message):
 response=run_chatbot(data.message)
 return {"answer": response["answer"]}
 