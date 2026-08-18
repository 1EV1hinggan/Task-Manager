
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from fastapi import Depends
from dependencies import get_current_username


from database import SessionLocal
import crud
import auth
import auth_crud


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


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=100)


class LoginRequest(BaseModel):
    username: str
    password: str



@app.get("/tasks", response_model=list[TaskResponse])
def get_tasks(username: str = Depends(get_current_username)):
    with SessionLocal() as session:
        return crud.get_tasks(session)



@app.post("/tasks", response_model=TaskResponse, status_code=201)
def create_task(task_data: TaskCreate,
                username: str = Depends(get_current_username)):
    with SessionLocal() as session:
        return crud.create_task(session, task_data.title)



@app.put("/tasks/{task_id}", response_model=TaskResponse, responses={404: {"description": "Task not found"}})
def update_task(task_id: int,
                task_data: TaskUpdate,
                username: str = Depends(get_current_username)):
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
def delete_task(task_id: int,
                username: str = Depends(get_current_username)):
    with SessionLocal() as session:

        task = crud.get_task(session, task_id)

        if not task:
            raise HTTPException(
                status_code=404,
                detail="Task not found"
            )

        crud.delete_task(session, task)

        return

@app.post("/register")
def register(user_data: UserCreate):
    with SessionLocal() as session:

        existing_user = auth_crud.get_user_by_username(
            session,
            user_data.username
        )

        if existing_user:
            raise HTTPException(
                status_code=409,
                detail="Username already exists"
            )

        user = auth_crud.create_user(
            session,
            user_data.username,
            user_data.password
        )

        return {
            "message": "User registered successfully",
            "username": user.username
        }


@app.post("/login")
def login(login_data: LoginRequest):
    with SessionLocal() as session:

        user = auth_crud.get_user_by_username(
            session,
            login_data.username
        )

        if not user:
            raise HTTPException(
                status_code=401,
                detail="Invalid username or password"
            )

        if not auth.verify_password(
            login_data.password,
            user.password
        ):
            raise HTTPException(
                status_code=401,
                detail="Invalid username or password"
            )

        access_token = auth.create_access_token(
            user.username
        )

        return {
            "access_token": access_token,
            "token_type": "bearerpython -m uvicorn api:app --reload"
        }