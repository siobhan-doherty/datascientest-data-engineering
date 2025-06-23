from fastapi import FastAPI, Depends, Query, HTTPException, status
from typing import List
from models import Question
from auth import basic_auth
from data_loader import QUESTIONS
import random


api = FastAPI(
    title = "MCQ Service",
    description = "Serve randomised quiz questions",
    version = "1.0",
)

@api.get("/health", tags = ["utilities"], summary = "Health check")
def health():
    return {"status": "ok"}

@api.get(
    "/questions",
    response_model = List[Question],
    tags = ["questions"],
    summary = "Get a batch of random questions",
    responses = {
        401: {"description": "Unauthorised"},
        422: {"description": "Validation error"},
        404: {"description": "No questions found"},
    },
)
def get_questions(
    use: str = Query(..., description = "Test type (e.g. MCQ)"),
    subject: List[str] = Query(..., description = "One or more subjects"),
    count: int = Query(..., description = "Number of questions (5, 10, 20)"),
    user: str = Depends(basic_auth),
):
    # enforce exactly 5, 10 or 20
    if count not in (5, 10, 20):
        raise HTTPException(
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail = "Count must be 5, 10 or 20",
        )
    # filter
    pool = [q for q in QUESTIONS if q["use"] == use and q["subject"] in subject]
    if not pool:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "No questions match")
    return random.sample(pool, min(count, len(pool)))

@api.post(
    "/questions",
    response_model = Question,
    status_code = status.HTTP_201_CREATED,
    tags = ["questions"],
    summary = "Create a new question (admin only)",
    responses = {
        401: {"description": "Unauthorised"},
        403: {"description": "Forbidden - not admin"},
    },
)
def create_question(
    q: Question,
    user: str = Depends(basic_auth),
):
    if user != "admin":
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Admins only")
    QUESTIONS.append(q.dict())
    return q
