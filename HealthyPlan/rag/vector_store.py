from functools import lru_cache
from pathlib import Path

import chromadb
import numpy as np
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from .config import (
    COLLECTION_NAME,
    CONDITION_ROUTER_COLLECTION_NAME,
    EMBEDDING_BATCH_SIZE,
    MODEL_NAME,
    VECTOR_PATH,
)


@lru_cache(maxsize=1)
def get_embedding_model():
    print(f"Loading embedding model: {MODEL_NAME}")

    embedding_model = HuggingFaceEmbeddings(
        model_name=MODEL_NAME,
        model_kwargs={
            "local_files_only": True,
        },
        encode_kwargs={
            "batch_size": EMBEDDING_BATCH_SIZE,
            "normalize_embeddings": True,
        },
        query_encode_kwargs={
            "batch_size": EMBEDDING_BATCH_SIZE,
            "normalize_embeddings": True,
        },
        show_progress=True,
    )

    return embedding_model


@lru_cache(maxsize=1)
def get_chroma_client():
    Path(VECTOR_PATH).mkdir(
        parents=True,
        exist_ok=True,
    )

    client = chromadb.PersistentClient(
        path=VECTOR_PATH,
    )

    return client


@lru_cache(maxsize=1)
def get_collection():
    client = get_chroma_client()

    collection = client.get_collection(
        name=COLLECTION_NAME,
    )

    return collection


@lru_cache(maxsize=1)
def get_condition_router_collection():
    client = get_chroma_client()

    collection = client.get_collection(
        name=CONDITION_ROUTER_COLLECTION_NAME,
    )

    return collection


@lru_cache(maxsize=1)
def get_vector_store():
    vector_store = Chroma(
        client=get_chroma_client(),
        collection_name=COLLECTION_NAME,
        embedding_function=get_embedding_model(),
    )

    return vector_store


@lru_cache(maxsize=1)
def get_condition_router_vector_store():
    vector_store = Chroma(
        client=get_chroma_client(),
        collection_name=CONDITION_ROUTER_COLLECTION_NAME,
        embedding_function=get_embedding_model(),
    )

    return vector_store


def embedding_texts(texts):
    if isinstance(texts, str):
        texts = [texts]

    if not isinstance(texts, (list, tuple)):
        raise TypeError("Texts must be a string, list or tuple")

    normalized_texts = []

    for text in texts:
        if not isinstance(text, str):
            raise TypeError("Every text must be a string")

        normalized_text = " ".join(
            text.strip().split()
        )

        if not normalized_text:
            raise ValueError("Text cannot be empty")

        normalized_texts.append(normalized_text)

    if not normalized_texts:
        raise ValueError("Texts cannot be empty")

    embedding_model = get_embedding_model()

    embeddings = embedding_model.embed_documents(
        normalized_texts
    )

    return np.asarray(
        embeddings,
        dtype=np.float32,
    )