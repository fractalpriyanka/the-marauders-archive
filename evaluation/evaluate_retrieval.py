import json
from src.retrieval.retriever import retrieve

def evaluate_retrieval():
    with open("evaluation/eval_questions.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    total = len(data)
    hit = 0

    for item in data:
        chunks = retrieve(item["question"])
        # context = " ".join(c["text"].lower() for c in chunks)
        context = " ".join(
                (c["text"] + " " + " ".join(c.get("facts", []))).lower()
                for c in chunks
            )


        if item["answer"].lower() in context:
            hit += 1
            status = "✅ FOUND"
        else:
            status = "❌ MISSING"

        print(f"[{status}] Q{item['id']}: {item['question']}")

    print("\nRetrieval Recall@K:", hit / total)

if __name__ == "__main__":
    evaluate_retrieval()
