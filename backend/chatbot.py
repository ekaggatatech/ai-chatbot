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
Answer using the context that is provide to you.
and If you don't find the answer then say "Sorry, I don't have this information right now ."
And if user ask the question which is not related to the Hourmaker website then simply say "Sorry, I can't help you with this."
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
        #Ask the Gemini to generate the answer
        response = client.models.generate_content(
            model=LLM_MODEL,
            contents=prompt
        )
        return response.text
    except Exception as e:
      #If Gemini crashes , print the error details 
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
    # Send the question and collected text to Gemini to get the AI response
    ai_answer = get_gemini_answer(question, context)
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
