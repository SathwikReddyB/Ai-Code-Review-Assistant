from services.indexing.file_loader import load_repository_files
from services.indexing.chunker import chunk_documents
from services.indexing.embeddings import create_embeddings
from services.indexing.faiss_store import create_faiss_index, save_index

import pickle


def index_repository(repo_path, repo_name):

    docs = load_repository_files(repo_path)

    chunks = chunk_documents(docs)

    with open(
        f"vector_store/{repo_name}_chunks.pkl",
        "wb"
    ) as f:
        pickle.dump(
            chunks[:1000],
            f
        )

    texts = [
        chunk.page_content
        for chunk in chunks[:1000]
    ]

    vectors = create_embeddings(texts)

    index = create_faiss_index(vectors)

    save_index(
        index,
        f"vector_store/{repo_name}.index"
    )

    return len(texts)