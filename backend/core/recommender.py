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

_retriever = None

def get_retriever():
    global _retriever
    if _retriever is None:
        embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
        vectorstore = Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=embeddings,
            persist_directory=CHROMA_PATH
        )
        _retriever = vectorstore.as_retriever(
            search_kwargs={
                "k": TOP_K_RESULTS,
                "filter": {"score": {"$gte": 6.0}}
            }
        )
    return _retriever

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
    ("system", """You are an expert anime curator with deep knowledge of anime across all eras, genres, and tones.

Your recommendations must match the EMOTIONAL and ATMOSPHERIC feel of what the user is asking for — not just genre tags.

Guidelines:
- Match TONE and FEELING first. A calm reflective anime is not the same as an action anime even if both are "fantasy"
- Prefer anime with high scores (7.5+) and well-known titles UNLESS the user specifically asks for hidden gems or obscure anime
- Draw on BOTH the database context below AND your own knowledge to give the best recommendations
- The database gives you accurate scores, genres, and synopses — use it for facts
- Your own knowledge fills in tonal and atmospheric nuance the database can't capture
- Never recommend anime that contradict the user's stated mood or vibe
- Be specific about WHY each recommendation matches — mention tone, pacing, characters, atmosphere
- If the user asks for one recommendation, give one. If they ask for many, give many. Match what they asked for.
- Keep your answer focused and human — not a generic list

Relevant anime from the database:
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
