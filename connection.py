import httpx
from pydantic import BaseModel

BASE_URL = "http://127.0.0.1:8000"


class ScoreItem(BaseModel):
    id: int
    score: int
    username: str


class ApiResponse(BaseModel):
    items: list[ScoreItem]


def get_user_max_scores(nickname: str) -> ApiResponse:
    r = httpx.get(f"{BASE_URL}/api/scores", params={"username": nickname})
    r.raise_for_status()
    return ApiResponse(**r.json())


def create_user(nickname: str, score: int):
    r = httpx.post(f"{BASE_URL}/api/scores", json={"username": nickname, "score": score})
    r.raise_for_status()


def update_user_max_scores(id: int, new_score: int):
    r = httpx.patch(f"{BASE_URL}/api/scores/{id}", json={"score": new_score})
    r.raise_for_status()
