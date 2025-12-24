import os
from dotenv import load_dotenv

load_dotenv()

# -------- Paths --------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

PDF_PATH = os.path.join(BASE_DIR, "data", "raw", "harrypotter.pdf")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")

PAGES_PATH = os.path.join(PROCESSED_DIR, "pages.json")
CHUNKS_PATH = os.path.join(PROCESSED_DIR, "chunks.json")
FAISS_INDEX_PATH = os.path.join(PROCESSED_DIR, "index.faiss")

# -------- Book order (image page → new book) --------
BOOK_SEQUENCE = [
    "Harry Potter and the Sorcerer’s Stone",
    "Harry Potter and the Chamber of Secrets",
    "Harry Potter and the Prisoner of Azkaban",
    "Harry Potter and the Goblet of Fire",
    "Harry Potter and the Order of the Phoenix",
    "Harry Potter and the Half-Blood Prince",
    "Harry Potter and the Deathly Hallows",
]

# -------- Chunking --------
NARRATIVE_CHUNK_SIZE = 400
NARRATIVE_OVERLAP = 100
POEM_MAX_LINES = 40

# -------- Embeddings --------
EMBEDDING_PROVIDER = "sentence-transformers"
EMBED_MODEL = "sentence-transformers/all-mpnet-base-v2"

# -------- Retrieval --------
TOP_K = 8

# -------- LLM (Generation only) --------
LLM_PROVIDER = "google-genai"
GEMINI_MODEL = "models/gemini-2.5-flash"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY not found in .env")