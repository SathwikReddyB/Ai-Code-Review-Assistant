from services.indexing.file_loader import load_repository_files
from services.indexing.chunker import chunk_documents
from services.indexing.embeddings import create_embeddings
from services.indexing.faiss_store import create_faiss_index

print("Loading files...")

docs = load_repository_files(
    "cloned_repos/react"
)

print(f"Files loaded: {len(docs)}")

print("Creating chunks...")

chunks = chunk_documents(docs)

print(f"Chunks created: {len(chunks)}")

print("Generating embeddings...")

texts = [chunk.page_content for chunk in chunks[:100]]

vectors = create_embeddings(texts)

print(f"Embeddings generated: {len(vectors)}")

print("Creating FAISS index...")

index = create_faiss_index(vectors)

print("FAISS index created.")

print(
    f"Total vectors stored: {index.ntotal}"
)