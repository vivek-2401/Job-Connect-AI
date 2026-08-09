import chromadb

client = chromadb.PersistentClient(path="data/chroma_db")

collection = client.get_or_create_collection(
    name="resume_collection"
)


def store_embeddings(chunks, embeddings):
    """
    Store chunks and embeddings in ChromaDB.
    """

    ids = [f"chunk_{i}" for i in range(len(chunks))]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings.tolist()
    )


def search(query_embedding, top_k=3):
    """
    Search similar chunks.
    """

    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=top_k
    )

    return results["documents"][0]
    