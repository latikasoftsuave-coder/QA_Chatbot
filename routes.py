from fastapi import APIRouter, Request
from pydantic import BaseModel
from services import ChatService
import uuid

router = APIRouter()

class Question(BaseModel):
    question: str

@router.post("/ask")
def ask_question(q: Question, request: Request, session_id: str = None):
    if session_id is None:
        session_id = str(uuid.uuid4())
    print(session_id)
    ChatService.store_user_message(session_id, q.question)
    messages = ChatService.get_last_messages(session_id, limit=10)
    answer = ChatService.generate_response(messages)
    ChatService.store_assistant_message(session_id, answer)
    return {"answer": answer}

@router.get("/history/{session_id}")
def get_history(session_id: str):
    return ChatService.get_all_messages(session_id)