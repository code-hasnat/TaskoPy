from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from .models import Base
from .routers import auth, users, projects, tasks

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TaskFlow API",
    description="A simple task management API",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(projects.router)
app.include_router(tasks.router)

@app.get("/")
def root():
    return {"message": "Welcome to TaskFlow API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}