from fastapi import APIRouter
from pydantic import BaseModel
from services import ChatService

router = APIRouter()

class Question(BaseModel):
    question: str

@router.post("/ask")
def ask_question(q: Question, session_id: str = None):
    return ChatService.process_user_question(q.question, session_id)

@router.get("/history/{session_id}")
def get_history(session_id: str):
    return ChatService.get_all_messages(session_id)