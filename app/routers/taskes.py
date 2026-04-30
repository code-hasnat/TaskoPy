from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import User, Task, Project
from ..schemas import TaskCreate, TaskResponse, TaskUpdate
from ..dependencies import get_current_user

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", response_model=TaskResponse)
def create_task(
    task: TaskCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    # Check if project exists and user owns it
    project = db.query(Project).filter(Project.id == task.project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    if project.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create tasks in this project"
        )
    
    # If assignee is specified, check if user exists
    if task.assignee_id:
        assignee = db.query(User).filter(User.id == task.assignee_id).first()
        if not assignee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assignee not found"
            )
    
    db_task = Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/", response_model=List[TaskResponse])
def get_tasks(
    project_id: int = None,
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    if project_id:
        # Check if user owns the project
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )
        
        if project.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view tasks in this project"
            )
        
        tasks = db.query(Task).filter(Task.project_id == project_id).all()
    else:
        # Get all tasks from user's projects
        user_projects = db.query(Project).filter(Project.owner_id == current_user.id).all()
        project_ids = [p.id for p in user_projects]
        tasks = db.query(Task).filter(Task.project_id.in_(project_ids)).all()
    
    return tasks

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # Check if user owns the project
    project = db.query(Project).filter(Project.id == task.project_id).first()
    if project.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this task"
        )
    
    return task

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int, 
    task_update: TaskUpdate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # Check if user owns the project
    project = db.query(Project).filter(Project.id == task.project_id).first()
    if project.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this task"
        )
    
    # Update task fields
    update_data = task_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)
    
    db.commit()
    db.refresh(task)
    return task

@router.delete("/{task_id}")
def delete_task(
    task_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # Check if user owns the project
    project = db.query(Project).filter(Project.id == task.project_id).first()
    if project.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this task"
        )
    
    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}