import os
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

HF_BASE_URL = "https://router.huggingface.co/v1"
LLM_MODEL = "Qwen/Qwen2.5-72B-Instruct"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

CHROMA_DIRECTORY = "./chroma_db"