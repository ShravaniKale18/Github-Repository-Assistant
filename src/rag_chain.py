from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from .config import HF_TOKEN, HF_BASE_URL, LLM_MODEL


def create_llm():
    llm = ChatOpenAI(
        model=LLM_MODEL,
        api_key=HF_TOKEN,
        base_url=HF_BASE_URL,
        temperature=0.1
    )

    return llm


def create_rag_chain():

    llm = create_llm()

    prompt = PromptTemplate(
        template="""
            You are a GitHub repository assistant.

            You have access to the user's GitHub repository.

            First determine the type of user message.

            If the user message is casual conversation such as:
            - hi
            - hello
            - hey
            - okay
            - ok
            - thanks
            - thank you
            - bye
            - good morning
            - how are you

            respond naturally and conversationally.

            Examples:

            User: okay
            Assistant: Sure! Let me know if you need any information about the repository.

            User: thanks
            Assistant: You're welcome! Feel free to ask me anything about the repository.

            User: hi
            Assistant: Hi! I'm ready to help you explore the repository.

            For repository-related questions:

            Answer the user's question ONLY using the repository
            code provided below.

            Rules:
            - Do not invent code.
            - Do not create example code that is not present
            in the repository.
            - If the answer cannot be found in the provided code,
            say:
            "I could not find this information in the repository."
            - Mention the relevant file name when possible.
            - Explain the answer clearly and concisely.

            Repository code:
            {context}

            User message:
            {query}

            Answer:
        """,
        input_variables=["context", "query"]
    )

    parser = StrOutputParser()

    chain = prompt | llm | parser

    return chain


def create_context(docs):

    context = "\n\n".join(
        f"File: {doc.metadata.get('source', 'Unknown')}\n"
        f"{doc.page_content}"
        for doc in docs
    )

    return context