import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

TEXTBOOKS_DIR = "textbooks"
VECTOR_DB_DIR = "vector_db"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

NUM_RETRIEVED_DOCS = 5

MODEL_NAME = "llama-3.1-8b-instant"