import os

# -------- Folder Structure --------
folders = [
    "app",
    "src",
    "src/ingestion",
    "src/chunking",
    "src/embeddings",
    "src/retrieval",
    "src/generation",
    "src/utils",
    "config",
    "data",
    "data/raw",
    "data/processed"
]

# -------- Files --------
files = [
    # App
    "app/main.py",
    "app/__init__.py",

    # Ingestion
    "src/ingestion/pdf_loader.py",
    "src/ingestion/__init__.py",

    # Chunking
    "src/chunking/chunker.py",
    "src/chunking/__init__.py",

    # Embeddings
    "src/embeddings/embedder.py",
    "src/embeddings/__init__.py",

    # Retrieval
    "src/retrieval/retriever.py",
    "src/retrieval/build_index.py",
    "src/retrieval/__init__.py",

    # Generation
    "src/generation/llm.py",
    "src/generation/__init__.py",

    # Utils
    "src/utils/logger.py",
    "src/utils/__init__.py",

    # Root src
    "src/__init__.py",

    # Config
    "config/settings.py",
    "config/__init__.py",

    # Root files
    "requirements.txt",
    "README.md"
]

# -------- Create folders --------
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# -------- Create files --------
for file in files:
    if not os.path.exists(file):
        with open(file, "w", encoding="utf-8") as f:
            pass

print("✅ Project structure with __init__.py created successfully")
