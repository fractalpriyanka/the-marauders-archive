# import json
# from src.retrieval.retriever import retrieve
# from src.generation.llm import generate_answer

# def evaluate_answers():
#     with open("evaluation/eval_questions.json", "r", encoding="utf-8") as f:
#         data = json.load(f)

#     for item in data:
#         chunks = retrieve(item["question"])
#         context = "\n".join(c["text"] for c in chunks)

#         answer = generate_answer(context, item["question"])

#         print("\nQ:", item["question"])
#         print("Expected:", item["answer"])
#         print("Model:", answer)

# if __name__ == "__main__":
#     evaluate_answers()


# import json
# import time
# from src.retrieval.retriever import retrieve
# from src.generation.llm import generate_answer

# def evaluate_answers():
#     with open("evaluation/eval_questions.json", "r", encoding="utf-8") as f:
#         data = json.load(f)

#     for idx, item in enumerate(data, start=1):
#         chunks = retrieve(item["question"])

#         # limit context size (see Fix 2)
#         context = "\n".join(c["text"] for c in chunks[:3])

#         answer = generate_answer(context, item["question"])

#         print(f"\n[{idx}] Q:", item["question"])
#         print("Expected:", item["answer"])
#         print("Model:", answer)

#         time.sleep(3)  # ⬅️ CRITICAL (2–4 sec recommended)

# if __name__ == "__main__":
#     evaluate_answers()




import json
import time
from src.retrieval.retriever import retrieve
from src.generation.llm import generate_answer

MAX_QUESTIONS = 5

def trim_context(chunks, max_chars=1800):
    context = ""
    for c in chunks:
        text = c["text"].strip()
        if len(context) + len(text) > max_chars:
            break
        context += text + "\n"
    return context

def evaluate_answers():
    with open("evaluation/eval_questions.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    for idx, item in enumerate(data):
        if idx == MAX_QUESTIONS:
            print("🛑 Evaluation batch finished. Rerun to continue.")
            break

        chunks = retrieve(item["question"])
        context = trim_context(chunks)

        try:
            answer = generate_answer(context, item["question"])
        except Exception as e:
            print("⚠️ Gemini limit hit. Sleeping 20s...")
            time.sleep(20)
            answer = generate_answer(context, item["question"])

        print(f"\n[{idx+1}] Q:", item["question"])
        print("Expected:", item["answer"])
        print("Model:", answer)

        time.sleep(6)  # ⬅️ DO NOT REDUCE

if __name__ == "__main__":
    evaluate_answers()
