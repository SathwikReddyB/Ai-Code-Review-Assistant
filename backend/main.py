from fastapi import FastAPI
from routes.auth import router as auth_router
from routes.repository import router as repo_router

app = FastAPI()

app.include_router(
    auth_router,
    prefix="/api/auth",
    tags=["Authentication"]
)

app.include_router(
    repo_router,
    prefix="/api/repos",
    tags=["Repositories"]
)