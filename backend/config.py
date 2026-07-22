import os
from dotenv import load_dotenv
load_dotenv()

GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")
CHROMA_PATH="./embedding/chroma_db"
COLLECTION_NAME="hourmaker_docs"
EMBEDDING_MODEL="all-MiniLM-L6-v2"
LLM_MODEL="gemini-3.1-flash-lite"
TOP_K=3