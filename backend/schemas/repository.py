from pydantic import BaseModel

class GithubRepoRequest(BaseModel):
    github_url: str