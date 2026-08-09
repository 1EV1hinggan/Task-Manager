from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from database import SessionLocal
import crud



app = FastAPI()



class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)



class TaskUpdate(BaseModel):
    completed: bool



class TaskResponse(BaseModel):
    id: int
    title: str
    completed: bool

    class Config:
        from_attributes = True




@app.get("/tasks", response_model=list[TaskResponse])
def get_tasks():
    with SessionLocal() as session:
        return crud.get_tasks(session)



@app.post("/tasks", response_model=TaskResponse, status_code=201)
def create_task(task_data: TaskCreate):
    with SessionLocal() as session:
        return crud.create_task(session, task_data.title)



@app.put("/tasks/{task_id}", response_model=TaskResponse, responses={404: {"description": "Task not found"}})
def update_task(task_id: int, task_data: TaskUpdate):
    with SessionLocal() as session:

        task = crud.get_task(session, task_id)

        if not task:
            raise HTTPException(
                status_code=404,
                detail="Task not found"
            )

        return crud.update_task(
            session,
            task,
            task_data.completed
        )



@app.delete("/tasks/{task_id}", status_code=204, responses={404: {"description": "Task not found"}})
def delete_task(task_id: int):
    with SessionLocal() as session:

        task = crud.get_task(session, task_id)

        if not task:
            raise HTTPException(
                status_code=404,
                detail="Task not found"
            )

        crud.delete_task(session, task)

        return
