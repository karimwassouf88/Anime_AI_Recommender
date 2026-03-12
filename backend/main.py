
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from core.recommender import get_recommendation

# App
app=FastAPI()

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request and Response Models
class ChatRequest(BaseModel):
    message: str
    session_id: str

class ChatResponse(BaseModel):
    reply:str

# Server Check
@app.get("/health")
def health():
    return{"status":"ok"}

# Main Endpoint (take req send res)
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    reply = await get_recommendation(request.message, request.session_id)
    return ChatResponse(reply=reply)