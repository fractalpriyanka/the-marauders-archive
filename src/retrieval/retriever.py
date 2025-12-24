import json
import faiss
import numpy as np
import re
from sentence_transformers import SentenceTransformer
from typing import List, Dict

from config.settings import (
    CHUNKS_PATH,
    FAISS_INDEX_PATH,
    TOP_K,
    EMBED_MODEL
)

# -------------------------------------------------
# Load once (important for speed)
# -------------------------------------------------
model = SentenceTransformer(EMBED_MODEL)
index = faiss.read_index(FAISS_INDEX_PATH)

with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
    CHUNKS = json.load(f)

# Lookup by chunk_id
CHUNK_BY_ID = {c["chunk_id"]: c for c in CHUNKS}

# Chapter-wise index
CHAPTER_MAP = {}
for c in CHUNKS:
    key = (c["book"], c["chapter_id"])
    CHAPTER_MAP.setdefault(key, []).append(c)

# Ensure correct order inside chapter
for key in CHAPTER_MAP:
    CHAPTER_MAP[key].sort(key=lambda x: x["page_no"])


# -------------------------------------------------
# Query normalization (🔧 requested change)
# -------------------------------------------------
def normalize_query(query: str) -> str:
    query = query.lower()
    query = re.sub(r"\d", "", query)              # remove digits (lett5ers → letters)
    query = re.sub(r"[^a-z\s]", " ", query)       # remove punctuation
    query = re.sub(r"\s+", " ", query).strip()
    return query


# -------------------------------------------------
# Neighbor expansion (chapter-safe)
# -------------------------------------------------
def expand_with_neighbors(chunk: Dict, window: int) -> List[Dict]:
    key = (chunk["book"], chunk["chapter_id"])
    chapter_chunks = CHAPTER_MAP.get(key, [])

    idx = next(
        (i for i, c in enumerate(chapter_chunks)
         if c["chunk_id"] == chunk["chunk_id"]),
        None
    )

    if idx is None:
        return [chunk]

    start = max(0, idx - window)
    end = min(len(chapter_chunks), idx + window + 1)

    return chapter_chunks[start:end]


# -------------------------------------------------
# Main retrieval
# -------------------------------------------------
def retrieve(query: str) -> List[Dict]:
    # -------- Normalize query --------
    norm_query = normalize_query(query)

    # -------- Embed query --------
    q_vec = model.encode(
        [norm_query],
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    # -------- Semantic search --------
    _, indices = index.search(
        q_vec.astype("float32"),
        TOP_K
    )

    hits = [CHUNK_BY_ID[i] for i in indices[0]]

    # -------- Adaptive window --------
    # Emergent facts need more context
    window = 3 if len(hits) < 5 else 2

    expanded = []
    seen = set()

    for chunk in hits:
        neighbors = expand_with_neighbors(chunk, window=window)
        for n in neighbors:
            if n["chunk_id"] not in seen:
                expanded.append(n)
                seen.add(n["chunk_id"])

    # -------- Light lexical anchoring (boost exact phrases) --------
    boosted = []
    for c in expanded:
        if norm_query in c["text"].lower():
            boosted.append(c)

    if boosted:
        expanded = boosted + [
            c for c in expanded if c not in boosted
        ]

    # -------- Final ordering --------
    expanded.sort(
        key=lambda c: (
            c["book"],
            c["chapter_id"],
            c["page_no"],
            c["chunk_id"]
        )
    )

    return expanded


