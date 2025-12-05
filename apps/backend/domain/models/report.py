from typing import Annotated, List
from bson import ObjectId
from pydantic import BaseModel, Field

from priority_enum import PriorityEnum


class Scores(BaseModel):
    privacy: Annotated[int, Field(gt=0, le=100)] = 0
    fairness: Annotated[int, Field(gt=0, le=100)] = 0
    readability: Annotated[int, Field(gt=0, le=100)] = 0


class RiskyClause(BaseModel):
    title: str
    priority: PriorityEnum


class Report(BaseModel):
    report_id: str = Field(default_factory=lambda: str(ObjectId()))
    scores: Scores
    summary: str
    risky_clauses: List[RiskyClause]
    detected_phrases: List[str]
    reason: str
