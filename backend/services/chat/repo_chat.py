import pickle

from services.indexing.embeddings import (
    create_query_embedding
)

from services.indexing.faiss_store import (
    load_index,
    search_index
)

from services.chat.openai_service import generate_answer


def retrieve_context(repo_name, question):

    index = load_index(
        f"vector_store/{repo_name}.index"
    )

    with open(
        f"vector_store/{repo_name}_chunks.pkl",
        "rb"
    ) as f:
        chunks = pickle.load(f)

    query_vector = create_query_embedding(
        question
    )

    # Retrieve only the most relevant chunks
    results = search_index(
        index,
        query_vector,
        top_k=3
    )

    context_parts = []

    for idx in results:

        if idx < len(chunks):

            context_parts.append(
                chunks[idx].page_content
            )

    context = "\n\n".join(context_parts)

    # Keep context small enough for TinyLlama
    return context[:2500]


def ask_repository(repo_name, question):

    context = retrieve_context(
        repo_name,
        question
    )

    print("\n===== QUESTION =====")
    print(question)

    print("\n===== CONTEXT =====")
    print(context[:1000])

    print("\n===== CONTEXT LENGTH =====")
    print(len(context))

    prompt = f"""
You are an expert software engineer.

Use ONLY the repository context below to answer the question.

If the answer is not present in the repository context, respond exactly with:

I could not find that information in the repository.

Repository Context:
{context}

Question:
{question}

Answer:
"""

    answer = generate_answer(prompt)

    return answer.strip()