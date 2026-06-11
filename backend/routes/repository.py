from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models.repository import Repository
from schemas.repository import GithubRepoRequest

from routes.auth import get_current_user
from fastapi import HTTPException

import os
import git

from services.indexing.index_repository import index_repository

router = APIRouter()

# Endpoint to add a GitHub repository for the current user
@router.post("/github")
def add_github_repository(
    repo: GithubRepoRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    repo_name = repo.github_url.rstrip("/").split("/")[-1]

    new_repo = Repository(
        user_id=current_user.id,
        repo_name=repo_name,
        github_url=repo.github_url,
        status="PENDING"
    )

    db.add(new_repo)
    db.commit()
    db.refresh(new_repo)

    return {
        "message": "Repository added successfully",
        "repo_id": new_repo.id,
        "repo_name": new_repo.repo_name
    }

# Endpoint to list all repositories for the current user
@router.get("/")
def get_user_repositories(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    repos = db.query(Repository).filter(
        Repository.user_id == current_user.id
    ).all()

    return repos

# Endpoint to get details of a specific repository by ID
@router.get("/{repo_id}")
def get_repository(
    repo_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    repo = db.query(Repository).filter(
        Repository.id == repo_id,
        Repository.user_id == current_user.id
    ).first()

    if not repo:
        raise HTTPException(
            status_code=404,
            detail="Repository not found"
        )

    return repo

# Endpoint to clone the GitHub repository and update its status
@router.post("/{repo_id}/clone")
def clone_repository(
    repo_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    repo = db.query(Repository).filter(
        Repository.id == repo_id,
        Repository.user_id == current_user.id
    ).first()

    if not repo:
        raise HTTPException(
            status_code=404,
            detail="Repository not found"
        )

    if not repo.github_url:
        raise HTTPException(
            status_code=400,
            detail="No GitHub URL available"
        )

    clone_path = f"cloned_repos/{repo.repo_name}"

    if os.path.exists(clone_path):
        return {
            "message": "Repository already cloned",
            "path": clone_path
        }

    git.Repo.clone_from(
        repo.github_url,
        clone_path
    )

    repo.upload_path = clone_path
    repo.status = "READY"

    db.commit()

    return {
        "message": "Repository cloned successfully",
        "path": clone_path
    }

# Endpoint to index the cloned repository and create vector embeddings
@router.post("/{repo_id}/index")
def index_repo(
    repo_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    repo = db.query(Repository).filter(
        Repository.id == repo_id,
        Repository.user_id == current_user.id
    ).first()

    if not repo:
        raise HTTPException(
            status_code=404,
            detail="Repository not found"
        )

    count = index_repository(
        repo.upload_path,
        repo.repo_name
    )

    repo.indexed = True
    repo.status = "INDEXED"

    db.commit()

    return {
        "message": "Repository indexed successfully",
        "chunks_indexed": count
    }