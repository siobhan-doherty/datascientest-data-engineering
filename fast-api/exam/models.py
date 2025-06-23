from pydantic import BaseModel
from typing import List, Optional


class Question(BaseModel):
    question: str
    subject: str
    use: str
    correct: List[str]
    answerA: str
    answerB: str
    answerC: str
    answerD: Optional[str] = None
