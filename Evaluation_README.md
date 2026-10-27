# RAG Evaluation — The Marauder’s Archive

## 1. Evaluation Overview

| Property | Details |
|---|---|
| Evaluation type | Offline evaluation |
| Dataset | Combined PDF containing all seven Harry Potter books |
| Number of evaluation questions | 15 |
| Evaluation approaches | RAGAS evaluation and separate local retrieval evaluation |
| LLM used for RAGAS evaluation | Google Gemini `gemini-3.5-flash-lite` |
| Embedding model | `sentence-transformers/all-mpnet-base-v2` |
| Embedding dimensions | 768 |
| Vector database | FAISS |
| Execution environment | CPU |
| Main evaluation focus | Retrieval quality, context coverage, faithfulness, answer relevance, and latency |

The evaluation uses two separate approaches:

1. **RAGAS evaluation:** Measures context precision, context recall, faithfulness, and answer relevancy.
2. **Local retrieval evaluation:** Measures retrieval performance against manually verified gold evidence, along with retrieval latency.

The two approaches use separate evaluation runs and should be interpreted independently.

---

## 2. Evaluation Dataset

A total of **15 questions** were used to evaluate the RAG system against the combined Harry Potter book collection.

### Evaluation Questions

| ID | Evaluation Question |
|---|---|
| Q1 | Where does Dumbledore's Army hold meetings? |
| Q2 | What did Dolores Umbridge force Harry to write during detention? |
| Q3 | What kind of car does Arthur Weasley drive? |
| Q4 | How old was Neville when his magic first appeared? |
| Q5 | Who tells Harry about the Marauder's Map? |
| Q6 | What phrase activates the Marauder's Map? |
| Q7 | Where is the entrance to the Chamber of Secrets? |
| Q8 | Who destroys Tom Riddle's diary? |
| Q9 | What is the full name of Professor Dumbledore? |
| Q10 | What song is sung at Hogwarts at the start of term? |
| Q11 | Who gives Harry the Invisibility Cloak? |
| Q12 | Where does Harry first meet Dobby? |
| Q13 | How many Horcruxes did Voldemort create? |
| Q14 | Who were the creators of the Marauder's Map? |
| Q15 | What is the name of Hagrid's dog? |

### Question Diversity

The questions primarily test factual retrieval across the book collection. Their categories overlap because a single question can test more than one type of information.

| Question category | Number of questions |
|---|---:|
| Factual retrieval and specific details | 15 |
| Names and relationships | 7 |
| Locations | 4 |
| Objects, phrases, and specific text | 4 |
| Events and actions | 5 |
| Numerical details | 1 |
| Unanswerable questions | 0 |

**Note:** These categories are overlapping, not mutually exclusive. Their counts should not be added to obtain the total number of questions.

The dataset does not currently include a dedicated set of unanswerable questions, so the evaluation does not establish how reliably the system refuses to answer when the source material lacks the required information.

---

## 3. RAGAS Evaluation

RAGAS was used to evaluate the quality of the generated answers and the retrieved context across the 15 questions.

### Metrics and Results

| Metric | Score | What It Measures |
|---|---:|---|
| Context Precision | 0.3556 | How relevant the retrieved context is to answering the question |
| Context Recall | 0.4000 | How much of the required reference information is captured in the retrieved context |
| Faithfulness | 0.7222 | How well the generated answer is supported by the retrieved context |
| Answer Relevancy | 0.4501 | How relevant the generated answer is to the user's question |

### Interpretation

- **Context Precision — 0.3556:** The relatively low score suggests that retrieved context often includes information that is not sufficiently relevant to the question.
- **Context Recall — 0.4000:** The score suggests that the retrieved context frequently misses some of the information required to answer the questions.
- **Faithfulness — 0.7222:** The generated answers show some alignment with the retrieved context, but unsupported statements and grounding errors still require investigation.
- **Answer Relevancy — 0.4501:** The score suggests that some answers may not address the question directly enough.

These scores indicate areas for investigation rather than proving that individual answers are correct or incorrect. They are evaluation scores, **not percentages of factual accuracy**.

---

## 4. Local Retrieval Evaluation

A separate local evaluation was used to measure retrieval performance against manually verified gold evidence.

### Retrieval Configuration

| Property | Value |
|---|---|
| Number of evaluation questions | 15 |
| Retrieval Top-K | 8 |
| Gold evidence verified | 2 questions |
| Gold evidence pending verification | 13 questions |
| Mean retrieval latency | 36.600 ms/query |
| P95 retrieval latency | 45.819 ms |

### Retrieval Metrics

The gold evidence was verified for Q1 and Q10. The remaining 13 questions do not yet have verified gold evidence for a complete retrieval evaluation.

| Metric | Result | Evaluation Scope |
|---|---:|---|
| Hit Rate@5 | 0.50 | 2 questions with verified gold evidence |
| Recall@1 | 0.50 | 2 questions with verified gold evidence |
| Recall@3 | 0.50 | 2 questions with verified gold evidence |
| Mean Reciprocal Rank (MRR) | 0.50 | 2 questions with verified gold evidence |

**Important:** These retrieval scores are based on only two questions with verified gold evidence. They should not be interpreted as representative performance across the full 15-question dataset.

### Question-Level Retrieval Findings

| Question ID | Finding |
|---|---|
| Q1 | The verified gold evidence was not found within the retrieved Top-8 results. |
| Q10 | The verified gold evidence was ranked first in the retrieved results. |
| Q2–Q9 and Q11–Q15 | Gold evidence verification is pending; retrieval performance cannot yet be reliably scored for these questions. |

### Retrieval Latency

| Latency Metric | Result |
|---|---:|
| Mean retrieval latency | 36.600 ms/query |
| P95 retrieval latency | 45.819 ms |

These latency results describe the local retrieval evaluation run and its configuration. They do not represent total end-to-end response time.

---

## 5. Latency Evaluation

Latency was recorded separately during the RAGAS evaluation and local retrieval evaluation.

| Evaluation Run | Metric | Result |
|---|---|---:|
| RAGAS evaluation | Mean retrieval latency | 44.53 ms/question |
| RAGAS evaluation | Mean answer-generation latency | 1,684.33 ms/question |
| Local retrieval evaluation | Mean retrieval latency | 36.600 ms/query |
| Local retrieval evaluation | P95 retrieval latency | 45.819 ms |

**Interpretation notes:**

- The RAGAS evaluation measured retrieval and answer-generation latency separately.
- The local retrieval evaluation measured retrieval latency without representing the full answer-generation pipeline.
- The two retrieval latency measurements come from separate runs and configurations. They should not be treated as a direct benchmark comparison.
- The mean answer-generation latency is not a complete end-to-end latency measurement unless all other pipeline stages are included.

---

## 6. Evaluation Summary

| Evaluation Area | Result | Status |
|---|---|---|
| Context Precision | 0.3556 | Measured |
| Context Recall | 0.4000 | Measured |
| Faithfulness | 0.7222 | Measured |
| Answer Relevancy | 0.4501 | Measured |
| Local Hit Rate@5 | 0.50 | Measured on 2 verified questions |
| Local Recall@1 | 0.50 | Measured on 2 verified questions |
| Local Recall@3 | 0.50 | Measured on 2 verified questions |
| Local MRR | 0.50 | Measured on 2 verified questions |
| Mean local retrieval latency | 36.600 ms/query | Measured |
| P95 local retrieval latency | 45.819 ms | Measured |
| Mean RAGAS-harness retrieval latency | 44.53 ms/question | Measured |
| Mean answer-generation latency | 1,684.33 ms/question | Measured |
| Full-dataset local retrieval performance | Not established | Gold evidence verification incomplete |
| Local answer correctness | Not established | No complete manual answer-correctness evaluation |
| Category-level performance | Not measured | Requires category-wise scoring |

---

## 7. Limitations and Missing Evaluation Coverage

The current evaluation has the following limitations:

1. **Small evaluation dataset:** Only 15 questions were used. The results may not represent performance across all seven books or all possible question types.
2. **Incomplete gold evidence verification:** Gold evidence has been verified for only 2 of the 15 questions. Local retrieval metrics are therefore preliminary.
3. **No dedicated unanswerable questions:** The evaluation does not measure the system's ability to identify questions that cannot be answered from the source material.
4. **No complete local answer-correctness assessment:** The current results do not establish a manually verified answer accuracy score across all questions.
5. **No category-level metric breakdown:** Performance has not been calculated separately for names, locations, events, objects, numerical details, or other question categories.
6. **Metric interpretation:** RAGAS scores are useful indicators of retrieval and generation quality but should not be interpreted as direct factual-accuracy percentages.
7. **Reproducibility details:** Exact package versions, chunk size, chunk overlap, random seed, and all generation settings were not recorded in the available evaluation summary.
8. **No complete end-to-end latency benchmark:** The reported latency measurements cover separate pipeline stages and evaluation runs.

---

## 8. Recommended Next Steps

| Priority | Action | Purpose |
|---|---|---|
| High | Verify gold evidence for the remaining 13 questions | Make local retrieval metrics representative of the full dataset |
| High | Inspect low Context Precision and Context Recall cases | Identify retrieval and chunking issues |
| High | Review low Answer Relevancy cases | Identify answers that do not directly address the question |
| High | Manually verify generated answers against the source books | Establish answer correctness more directly |
| Medium | Add unanswerable questions | Evaluate whether the system can avoid unsupported answers |
| Medium | Calculate retrieval metrics by question category | Identify strengths and weaknesses across question types |
| Medium | Record chunking, generation, and dependency configurations | Improve reproducibility |
| Medium | Measure complete end-to-end latency | Evaluate overall response performance |

---

## 9. Final Assessment

The current evaluation provides an initial assessment of retrieval and generation quality for The Marauder’s Archive.

The RAGAS results indicate that context retrieval and answer relevance need further investigation. Faithfulness is comparatively stronger than the other reported RAGAS metrics, but it does not establish factual correctness.

The separate local retrieval evaluation provides latency measurements and preliminary retrieval metrics. However, because gold evidence has been verified for only two questions, the local retrieval scores should be treated as preliminary rather than representative of the complete dataset.

**Overall status:** Initial evaluation completed; comprehensive local retrieval validation and answer-correctness verification remain pending.
