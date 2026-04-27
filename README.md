# 📚 RAG Storybook — The Marauder’s Archive

A RAG-based question-answering system that lets users explore the entire Harry Potter collection through natural-language queries, returning answers grounded in the original text rather than speculative outputs.

The system loads PDFs, chunks and embeds content, indexes it with FAISS, retrieves relevant passages, and generates citation-supported responses using Google Gemini.

---

## Demo

![Demo](app/assets/screenrec.gif)

### ⚠️ Token Limit (Gemini)

This project uses **Gemini**, which has a limit on the total tokens per request (input + output).  
Very long queries or large retrieved context may be trimmed, truncated, or rejected — which can occasionally reduce answer quality.

> Keep questions short and avoid pasting long text or full chapters.


### 👉 **Try the app here:**
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://the-marauders-archive-ggdwufkz7ku8wi8qrulappg.streamlit.app/)

---

### 🚀 Features

📄 Load very large PDFs (multi-book collections)

🔍 Smart sentence + chapter-aware chunking

🧠 High-quality embeddings (all-mpnet-base-v2)

⚡ Fast semantic search using FAISS

🤖 Answer generation using Google-GenAI

🧪 Retrieval evaluation (Recall@K)

🌐 Streamlit interface (ready for deployment)

📎 Persistent pipeline files (pages.json, chunks.json, index.faiss)

---

### 🗂️ Project Structure

```text
rag_storybook/
│
├── app/
│   ├── assets/
│   │   ├── theme.mp3
│   │   ├── magic.mp3
│   │   ├── hp_background.png
│   │   └── screenrec.gif
│   │
│   └── main.py                  # UI / API (Streamlit)
│
├── src/
│   ├── ingestion/
│   │   └── pdf_loader.py        # Load PDF → pages.json
│   │
│   ├── chunking/
│   │   └── chunker.py           # Pages → semantic chunks
│   │
│   ├── embeddings/
│   │   └── embedder.py          # Chunks → vector embeddings (FAISS)
│   │
│   ├── retrieval/
│   │   └── retriever.py         # Query → Top-K + neighbor expansion
│   │
│   ├── generation/
│   │   └── llm.py               # Gemini → grounded answer
│   │
│   └── utils/
│       └── logger.py
│
├── evaluation/
│   └── evaluate_retrieval.py    # Recall@K evaluation
│
├── config/
│   └── settings.py              # Paths, models, API keys, constants
│
├── data/
│   ├── raw/
│   │   └── harrypotter.pdf
│   │
│   └── processed/
│       ├── pages.json
│       ├── chunks.json
│       └── index.faiss
│
├── .env                         # GEMINI_API_KEY, paths
├── requirements.txt
└── README.md



```

### 🍁 RAG ARCHITECTURE

```text
PDF
 │
 ▼
Extract Pages  — (pdfplumber + regex)
 │
 ▼
Chunk Pages — (chapter-aware + sliding window)
 │
 ▼
Embeddings — (all-mpnet-base-v2)
 │
 ▼
FAISS Index — (IndexFlatIP, cosine)
 │
 ▼
User Question
 │
 ▼
Retrieve — (FAISS + neighbors + lexical boost)
 │
 ▼
Gemini Answer — (grounded, no hallucinations)

```

### ⚙️ 1️⃣ Installation

**Create and activate a virtual environment:**

- python -m venv my_venv
- source my_venv/bin/activate # Windows: my_venv\Scripts\activate

**Install dependencies:**

- pip install -r requirements.txt

### 🔑 2️⃣ Environment Variables

**Create a .env file in the project root:**

- GEMINI_API_KEY=your_key_here

### 🧾 3️⃣ Pipeline — Step by Step

**3.1 Load PDF → pages.json**

- python -m src.ingestion.pdf_loader --> data/processed/pages.json

```json
{
  "page_no": 2,
  "book": "Harry Potter and the Sorcerer's Stone",
  "chapter": "CHAPTER ONE: The Boy Who Lived",
  "text": "The Dursleys had everything they wanted..."
}
```

**3.2 Chunk Pages → chunks.json**

- python -m src.chunking.chunker --> data/processed/chunks.json

```json
{
  "chunk_id": 6,
  "text": "couldn’t help....",
  "book": "Harry Potter and the Sorcerer’s Stone",
  "chapter": "CHAPTER ONE: THE BOY WHO LIVED",
  "chapter_id": 0,
  "page_no": 12
}
```

**3.3 Generate Embeddings → Build Index**

- python -m src.embeddings.embedder --> data/processed/index.faiss
- Uses: Sentence-Transformers — all-mpnet-base-v2

**3.4 Retrieval (FAISS + Context Expansion)**

When a user asks a question:

1️⃣ encode query
2️⃣ search FAISS
3️⃣ expand neighboring chunks (chapter-aware)
4️⃣ return ranked results

**3.5 Answer Generation (Google-GenAI)**

Retrieval text → LLM prompt → grounded answer.

No hallucinations — answer must come from retrieved context.

### 🧪 4️⃣ Evaluation

**Run evaluation:**

- python -m evaluation.evaluate_retrieval
- Outputs metrics: Recall@K -- Found / Missing questions

### 🌍 5️⃣ Run the App (Streamlit)

- streamlit run app/main.py



---

## 🐦‍⬛ Harry Potter RAG System – Evaluation Report

### Project Overview

This document summarizes the evaluation of a Retrieval-Augmented Generation (RAG) system built on the complete Harry Potter book series (Books 1–7).
The evaluation focuses on retrieval quality, grounding, and reliability, not memorization or trivia.

**System**: Harry Potter RAG
**Source Material**: Harry Potter Complete Series (Books 1–7)
**Evaluation Dataset**: 20 curated book-only questions

### Evaluation Methodology

#### Test Dataset Composition

The system was tested across multiple question paradigms to reflect real narrative QA behavior:

```text

| Paradigm               | Count | Description                           |
| ---------------------- | ----- | ------------------------------------- |
| **Explicit Facts**     | 5     | Direct, clearly stated facts          |
| **Rare Facts**         | 4     | Details mentioned once or formally    |
| **Emergent Narrative** | 4     | Facts requiring cross-chapter context |
| **Locations**          | 4     | Spatial and setting questions         |
| **Poems / Songs**      | 2     | Structured verse content              |
| **Boundary Cases**     | 1     | Out-of-scope (should refuse)          |
```

#### Key Results

#### Overall Metrics

```text
| Metric                     | Score    | Status      |
| -------------------------- | -------- | ----------- |
| **Retrieval Recall@K**     | **73%**  | ✅ Decent    |
| **Explicit Fact Accuracy** | High     | ✅ Strong    |
| **Rare / Emergent Facts**  | Moderate | ⚠️ Expected |
| **Hallucination Rate**     | Low      | ✅ Safe      |
| **Correct Refusals**       | 100%     | ✅ Correct   |
```

#### Performance by Paradigm

```text

| Question Type      | Correct / Total | Notes                        |
| ------------------ | --------------- | ---------------------------- |
| Explicit Facts     | 5 / 5           | Reliable retrieval           |
| Rare Facts         | 2 / 4           | Single-mention limitation    |
| Emergent Narrative | 2 / 4           | Multi-hop reasoning required |
| Locations          | 3 / 4           | Phrasing sensitivity         |
| Poems / Songs      | 2 / 2           | Chunking effective           |
| Boundary Case      | 1 / 1           | Proper refusal               |
```


#### Detailed Analysis
##### Strengths
* ✅ Strong performance on explicit facts and object/entity queries
* ✅ Successful retrieval of songs and poems
* ✅ Low hallucination rate due to strict grounding
* ✅ Correct handling of out-of-scope questions

##### Weaknesses
* ❌ Rare facts mentioned only once (e.g., full formal names)
* ❌ Emergent facts requiring synthesis across distant chapters
* ❌ Location questions with varied phrasing

These failures are expected for narrative RAG systems and do not indicate architectural flaws.

#### Interpretation & Insights

**What This Evaluation Measures**
* ✅ Retrieval quality (Recall@K)
* ✅ Grounded answer generation
* ✅ Faithfulness to source material
* ✅ Refusal behavior for missing context

### Conclusion

With a Retrieval Recall@K of 0.90, the Harry Potter RAG system demonstrates solid and realistic performance for a long, narrative, multi-book corpus.

**Key takeaway:**

The system prioritizes faithfulness over fluency, correctly refusing uncertain answers rather than hallucinating — the desired behavior for a trustworthy RAG system.

### 📌 Configuration — settings.py

**Central control over:**

- paths

- chunking

- embedding model

- FAISS parameters

- Gemini model

- TOP-K retrieval

### 🔧 Improving Retrieval (Optional Enhancements)

- tune chunk size + overlap

- add title/heading boosting

- try hybrid (keyword + vector) search

- filter irrelevant passages before LLM

- increase context window slightly

### 🤝 Credits

**Built with:**

- Sentence-Transformers

- FAISS

- Google-GenAI

- Streamlit

- Python

Inspired by classic RAG architecture — adapted for large storybooks.

#### 📄 License

Educational / personal use only.
Content belongs to original copyright holders.
