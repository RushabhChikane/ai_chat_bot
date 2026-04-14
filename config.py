import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# Paths
DATABASE_PATH = str(DATA_DIR / "shop.db")
CHROMA_DB_PATH = str(DATA_DIR / "chroma_db")

# Groq (free tier: 30 RPM, 14400 requests/day)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.3-70b-versatile"

# Embedding model (runs locally)
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
