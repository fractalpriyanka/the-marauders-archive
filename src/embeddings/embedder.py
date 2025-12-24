import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

from config.settings import (
    CHUNKS_PATH,
    FAISS_INDEX_PATH,
    EMBED_MODEL
)

def run():
    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    texts = [c["text"] for c in chunks]

    model = SentenceTransformer(EMBED_MODEL)
    vectors = model.encode(
        texts,
        batch_size=32,
        show_progress_bar=True,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    dim = vectors.shape[1]
    index = faiss.IndexFlatIP(dim)  # cosine similarity
    index.add(vectors.astype("float32"))

    faiss.write_index(index, FAISS_INDEX_PATH)

if __name__ == "__main__":
    run()
