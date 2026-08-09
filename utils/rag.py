from utils.chunking import chunk_text
from utils.embeddings import get_embeddings
from utils.vector_db import store_embeddings, search


def index_resume(resume_text):
    """
    Index resume into ChromaDB.
    """
    chunks = chunk_text(resume_text)

    if not chunks:
        return False

    embeddings = get_embeddings(chunks)
    store_embeddings(chunks, embeddings)

    return True


def retrieve_context(query):
    """
    Retrieve relevant resume context.
    """
    query_embedding = get_embeddings([query])[0]
    results = search(query_embedding)

    return "\n\n".join(results)