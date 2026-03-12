from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_message_histories import SQLChatMessageHistory
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import (
    GROQ_API_KEY,
    LLM_MODEL,
    EMBEDDING_MODEL,
    CHROMA_PATH,
    COLLECTION_NAME,
    MEMORY_DB_PATH,
    TOP_K_RESULTS
)

def get_retriever():
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vectorstore = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=CHROMA_PATH
    )
    return vectorstore.as_retriever(search_kwargs={"k": TOP_K_RESULTS})


def get_session_history(session_id: str) -> SQLChatMessageHistory:
    return SQLChatMessageHistory(
        session_id=session_id,
        connection=f"sqlite+aiosqlite:///{MEMORY_DB_PATH}",
        async_mode=True
    )

def build_chain():
    llm = ChatGroq(
        api_key=GROQ_API_KEY,
        model=LLM_MODEL,
        temperature=0.7
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert anime recommender. 
Use the following anime from the database to make personalized recommendations.
Be conversational, warm, and explain why each anime matches what the user is looking for.

Relevant anime from database:
{context}"""),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}")
    ])

    chain = prompt | llm | StrOutputParser()

    chain_with_memory = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="question",
        history_messages_key="history"
    )

    return chain_with_memory


async def get_recommendation(message: str, session_id: str) -> str:
    retriever = get_retriever()
    docs = retriever.invoke(message)
    context = "\n\n".join([doc.page_content for doc in docs])

    chain = build_chain()

    response = await chain.ainvoke(
        {
            "question": message,
            "context": context
        },
        config={"configurable": {"session_id": session_id}}
    )

    return response
