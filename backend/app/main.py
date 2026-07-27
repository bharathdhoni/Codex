from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models import init_db
from app.routers import solver_router
import os

app = FastAPI(
    title="Math Solver API",
    description="API for solving math problems with step-by-step solutions",
    version="1.0.0"
)

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite and Create React App defaults
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(solver_router.router, prefix="/api")


@app.on_event("startup")
def startup_event():
    """Initialize database on startup"""
    init_db()


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "Welcome to the Math Solver API",
        "docs": "/docs",
        "endpoints": {
            "solve": "POST /api/solve",
            "history": "GET /api/history"
        }
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
