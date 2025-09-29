import openai
from datetime import datetime
from db import SessionLocal, ChatMessage

class ChatService:

    @staticmethod
    def store_user_message(session_id: str, content: str):
        db = SessionLocal()
        try:
            user_msg = ChatMessage(session_id=session_id, role="user", content=content, timestamp=datetime.utcnow())
            db.add(user_msg)
            db.commit()
            db.refresh(user_msg)
            return user_msg
        finally:
            db.close()

    @staticmethod
    def store_assistant_message(session_id: str, content: str):
        db = SessionLocal()
        try:
            ai_msg = ChatMessage(session_id=session_id, role="assistant", content=content, timestamp=datetime.utcnow())
            db.add(ai_msg)
            db.commit()
            db.refresh(ai_msg)
            return ai_msg
        finally:
            db.close()

    @staticmethod
    def get_last_messages(session_id: str, limit: int = 10):
        db = SessionLocal()
        try:
            recent_messages = (
                db.query(ChatMessage)
                .filter(ChatMessage.session_id == session_id)
                .order_by(ChatMessage.id.desc())
                .limit(limit)
                .all()
            )
            return [{"role": m.role, "content": m.content} for m in reversed(recent_messages)]
        finally:
            db.close()

    @staticmethod
    def get_all_messages(session_id: str):
        db = SessionLocal()
        try:
            messages = (
                db.query(ChatMessage)
                .filter(ChatMessage.session_id == session_id)
                .order_by(ChatMessage.id)
                .all()
            )
            return [{"role": m.role, "content": m.content, "timestamp": m.timestamp.isoformat()} for m in messages]
        finally:
            db.close()

    @staticmethod
    def generate_response(messages: list):
        messages.insert(0, {"role": "system", "content": f"Current date: {datetime.utcnow().strftime('%Y-%m-%d')}"})
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        answer = response.choices[0].message.content
        return answer