import os

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from .config import (
    EMBEDDING_MODEL,
    CHROMA_DIRECTORY
)


def create_vector_store(chunks, repo_name):

    embedding_model = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

    repo_directory = os.path.join(
        CHROMA_DIRECTORY,
        repo_name
    )

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=repo_directory,
        collection_name="repository"
    )

    return vectorstore


def create_retriever(vectorstore):

    retriever = vectorstore.as_retriever(
        search_kwargs={
            "k": 4
        }
    )

    return retriever