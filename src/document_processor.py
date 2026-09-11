from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def create_documents(file_documents):

    documents = []

    for file in file_documents:

        document = Document(
            page_content=file["File Content"],
            metadata={
                "source": file["File Path"]
            }
        )

        documents.append(document)

    return documents


def split_documents(documents):

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = text_splitter.split_documents(documents)

    return chunks