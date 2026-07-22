import os
from dotenv import load_dotenv
from google import genai
from .config import GOOGLE_API_KEY, LLM_MODEL
from .rag import get_relevant_chunks

load_dotenv()

client = genai.Client(api_key=GOOGLE_API_KEY)

def get_gemini_answer(question: str, context: str):
    if not GOOGLE_API_KEY:
        return None
    try:
        prompt = f"""
You are the Hourmaker AI Assistant.
Answer using Markdown.

Rules:
- Use headings.
- Use bullet points.
- Keep paragraphs short.
- Bold important words.
- Never return one huge paragraph.
Context:
{context}

User Question:
{question}

Instructions:
- Use the context whenever it answers the question.
- If the message is just a greeting (Hi, Hello, Good Morning, etc.), ignore the context and greet naturally.
- If the user says thank you, reply politely.
- If the user says goodbye, say goodbye politely.
- If the question is unrelated to Hourmaker and isn't casual conversation, politely explain that you can help with Hourmaker-related questions.
- Format answers in Markdown using headings and bullet points where appropriate.
Answer:"""
        
        response = client.models.generate_content(
            model=LLM_MODEL,
            contents=prompt
        )
        return response.text
    except Exception as e:
      import traceback
      traceback.print_exc()
      print("\nGemini Error:", e)
      return None

def run_chatbot(question: str):
    chunks = get_relevant_chunks(question)
    if not chunks:
        return {
            "answer": "Sorry I don't have this information right now",
            "sources": []
        }
    
    # Format context and extract sources properly
    context = "\n\n".join([f"[{i+1}] {c['content']}" for i, c in enumerate(chunks)])
    sources = [c.get('metadata', {}).get('url', f"Document {i+1}") for i, c in enumerate(chunks)]
    
    ai_answer = get_gemini_answer(question, context)
    
    if ai_answer:
        answer = ai_answer
    else:
        # Fallback if Gemini fails
        answer = f"**Answer**\n{chunks[0]['content'][:400]}"
    
    return {
        "answer": answer,
        "sources": sources
    }
