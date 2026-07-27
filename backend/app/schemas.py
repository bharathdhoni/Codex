from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import datetime


class SolutionStep(BaseModel):
    """Represents a single step in the solution process"""
    step_number: int
    description: str
    expression: str
    latex: str


class SolveRequest(BaseModel):
    """Request model for solving a math problem"""
    expression: str = Field(..., description="The mathematical expression to solve")
    problem_type: Optional[Literal["algebra", "calculus", "auto"]] = "auto"
    detailed: bool = True


class SolveResponse(BaseModel):
    """Response model containing the solution"""
    success: bool
    final_answer: str
    final_answer_latex: str
    steps: List[SolutionStep]
    problem_type_detected: str
    error_message: Optional[str] = None


class HistoryItem(BaseModel):
    """Model for a history item"""
    id: int
    expression: str
    problem_type: str
    final_answer: str
    created_at: datetime

    class Config:
        from_attributes = True
