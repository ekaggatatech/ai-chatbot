import os
from dotenv import load_dotenv
from google import genai
from .config import GOOGLE_API_KEY, LLM_MODEL
from .rag import get_relevant_chunks
from google.genai import types
import re

load_dotenv()

client = genai.Client(api_key=GOOGLE_API_KEY)

def get_gemini_answer(question: str, context: str,history=None):
    if history is None:
        history=[]
    if not GOOGLE_API_KEY:
        return None
    try:
        gemini_history=[]
        for msg in history:
            role="user" if msg["role"]=="user" else"model"
            gemini_history.append(
                types.Content(
                    role=role,
                    parts=[
                        types.Part(text=msg["content"])
                    ]
                )
            )
        prompt = f"""
You are the Hourmaker AI Assistant.

Use BOTH:
1. The conversation history for remembering things the user has already told you.
2. The provided context for answering Hourmaker-related questions.

Rules:
1. If the user asks about something mentioned earlier in the conversation
  (for example: "What is my name?", "Tell me more about it."),
  answer from the conversation history.
2. Use the provided context only for Hourmaker information.
3. If the answer is not available in either the conversation history or the context,
  reply:
  "Sorry, I don't have this information right now."
Context:
{context}

User Question:
{question}

Instructions:
1. Use the context whenever it answers the question.
2.If the message is just a greeting (Hi, Hello, Good Morning, etc.), ignore the context and greet naturally.
3.If the user says thank you, reply politely.
4.If the user says goodbye, say goodbye politely.
5.If the question is unrelated to Hourmaker and isn't casual conversation, politely explain that you can help with Hourmaker-related questions.
6.Format answers using compact Markdown.
Rules:
  1. Never leave empty lines between bullet points.
  2.Never leave more than one blank line anywhere.
  3.Place headings immediately above their content.
  4. keep list compact.
  5.Do not add unnecessary spacing.

Answer:"""

        # Chat with history
        chat=client.chats.create(
            model=LLM_MODEL,
            history=gemini_history,
            config=genai.types.GenerateContentConfig(
                system_instruction=prompt
            )
        )
        # Send current question
        response=chat.send_message(question)
        answer = response.text
        # Remove 3 or more consecutive blank lines
        answer = re.sub(r"\n{3,}", "\n\n", answer)
        # Remove spaces on empty lines
        answer = "\n".join(line.rstrip() for line in answer.splitlines())
        return answer.strip()
    except Exception as e:
      #If Gemini crashes , print the error details 
      import traceback
      traceback.print_exc()
      print("\nGemini Error:", e)
      return None

def run_chatbot(question: str,history=None):
    if history is None:
        history=[]
    chunks = get_relevant_chunks(question)
    if not chunks:
        return {
            "answer": "Sorry I don't have this information right now",
            "sources": []
        }
    
    # Format context and extract sources properly
    context = "\n".join([f"[{i+1}] {c['content']}" for i, c in enumerate(chunks)])
    sources = [c.get('metadata', {}).get('url', f"Document {i+1}") for i, c in enumerate(chunks)]
    # Send the question and collected text to Gemini to get the AI response
    ai_answer = get_gemini_answer(question, context,history)
    #Use the Gemini answer if it worked , otherwise fallback and show raw text
    if ai_answer:
        answer = ai_answer
    else:
        # Fallback if Gemini fails
        answer = f"**Answer**\n{chunks[0]['content'][:400]}"
    
    return {
        "answer": answer,
        "sources": sources
    }
