from sentence_transformers import SentenceTransformer

# Load model only once
model = SentenceTransformer("all-MiniLM-L6-v2")


def get_embeddings(chunks):
    """
    Convert text chunks into embeddings.
    """
    return model.encode(chunks, convert_to_numpy=True)