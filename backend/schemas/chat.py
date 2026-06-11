from pydantic import BaseModel

class ChatRequest(BaseModel):
    repo_id: int
    question: str