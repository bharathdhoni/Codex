from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import json

from app.schemas import SolveRequest, SolveResponse, HistoryItem
from app.services.solver import MathSolver
from app.models import ProblemHistory, get_db

router = APIRouter()
solver = MathSolver()


@router.post("/solve", response_model=SolveResponse)
def solve_problem(request: SolveRequest, db: Session = Depends(get_db)):
    """
    Solve a math problem and return the solution with steps.
    
    - **expression**: The mathematical expression to solve
    - **problem_type**: Type of problem (algebra, calculus, derivative, integral, limit, or auto)
    - **detailed**: Whether to return detailed steps or just the answer
    """
    # Solve the problem
    result = solver.solve(request.expression, request.problem_type)
    
    # Save to history if successful
    if result["success"]:
        try:
            history_item = ProblemHistory(
                expression=request.expression,
                problem_type=result["problem_type_detected"],
                final_answer=result["final_answer"],
                steps=json.dumps(result["steps"])
            )
            db.add(history_item)
            db.commit()
            db.refresh(history_item)
        except Exception as e:
            # Don't fail the request if history saving fails
            pass
    
    return SolveResponse(**result)


@router.get("/history", response_model=List[HistoryItem])
def get_history(limit: int = 20, db: Session = Depends(get_db)):
    """Get the most recent solved problems from history"""
    items = db.query(ProblemHistory).order_by(
        ProblemHistory.created_at.desc()
    ).limit(limit).all()
    return items


@router.delete("/history")
def clear_history(db: Session = Depends(get_db)):
    """Clear all problem history"""
    db.query(ProblemHistory).delete()
    db.commit()
    return {"message": "History cleared successfully"}


@router.get("/history/{item_id}", response_model=HistoryItem)
def get_history_item(item_id: int, db: Session = Depends(get_db)):
    """Get a specific history item by ID"""
    item = db.query(ProblemHistory).filter(ProblemHistory.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="History item not found")
    return item
