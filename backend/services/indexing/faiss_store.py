import faiss
import numpy as np


def create_faiss_index(vectors):

    dimension = len(vectors[0])

    index = faiss.IndexFlatL2(dimension)

    index.add(
        np.array(vectors).astype("float32")
    )

    return index


def save_index(index, path):

    faiss.write_index(
        index,
        path
    )

def search_index(
    index,
    query_vector,
    top_k=5
):

    distances, indices = index.search(
        query_vector.astype("float32"),
        top_k
    )

    return indices[0]


def load_index(path):

    return faiss.read_index(path)

# def search_index(
#     index,
#     query_vector,
#     top_k=5
# ):

#     distances, indices = index.search(
#         query_vector.astype("float32"),
#         top_k
#     )

#     return indices[0]