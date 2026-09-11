from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from .config import (
    EMBEDDING_MODEL,
    CHROMA_DIRECTORY
)


def create_vector_store(chunks):

    embedding_model = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=CHROMA_DIRECTORY
    )

    return vectorstore


def create_retriever(vectorstore):

    retriever = vectorstore.as_retriever(
        search_kwargs={
            "k": 4
        }
    )

    return retriever