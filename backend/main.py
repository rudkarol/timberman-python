from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session

from backend.database import Base, engine, get_db


class MaxScore(Base):
    __tablename__ = "max_scores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    score = Column(Integer, default=0)


class ScoreCreate(BaseModel):
    username: str
    score: int


class ScoreUpdate(BaseModel):
    score: int


class ScoreResponse(BaseModel):
    id: int
    username: str
    score: int

    class Config:
        from_attributes = True


class ScoresListResponse(BaseModel):
    items: list[ScoreResponse]


app = FastAPI(title="Timberman Scores API")

Base.metadata.create_all(bind=engine)


@app.get("/api/scores", response_model=ScoresListResponse)
def get_scores(username: str = None, db: Session = Depends(get_db)):
    query = db.query(MaxScore)
    if username:
        query = query.filter(MaxScore.username == username)
    items = query.all()
    return ScoresListResponse(items=[ScoreResponse.model_validate(item) for item in items])


@app.post("/api/scores", response_model=ScoreResponse, status_code=201)
def create_score(data: ScoreCreate, db: Session = Depends(get_db)):
    record = MaxScore(username=data.username, score=data.score)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@app.patch("/api/scores/{score_id}", response_model=ScoreResponse)
def update_score(score_id: int, data: ScoreUpdate, db: Session = Depends(get_db)):
    record = db.query(MaxScore).filter(MaxScore.id == score_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Score not found")
    record.score = data.score
    db.commit()
    db.refresh(record)
    return record
