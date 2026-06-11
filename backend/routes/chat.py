from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from database import get_db

from models.repository import Repository

from schemas.chat import ChatRequest

from routes.auth import get_current_user

from services.chat.repo_chat import ask_repository

router = APIRouter()

@router.post("/")
def chat_with_repo(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    repo = db.query(Repository).filter(
        Repository.id == request.repo_id,
        Repository.user_id == current_user.id
    ).first()

    answer = ask_repository(
        repo.repo_name,
        request.question
    )

    return {
        "answer": answer
    }