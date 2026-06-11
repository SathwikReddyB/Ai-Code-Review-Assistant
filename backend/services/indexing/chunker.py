from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_documents(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = []

    for doc in documents:

        split_docs = splitter.create_documents(
            [doc["content"]],
            metadatas=[{"path": doc["path"]}]
        )

        chunks.extend(split_docs)

    return chunks