from fastapi import Depends, FastAPI, HTTPException, Query
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from database import get_db
from models import Task, User

app = FastAPI()


class UserCreate(BaseModel):
    name: str

class UserResponse(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db=Depends(get_db)):
    novo_usuario = User(
        name=user.name
    )

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    return novo_usuario

@app.get("/users", response_model=list[UserResponse])
def get_users(db=Depends(get_db)):
    stmt=select(User)
    result=db.execute(stmt)
    usuarios=result.scalars().all()

    return usuarios


class TaskCreate(BaseModel): 
    title: str
    description: str
    #completed: bool
    priority: int = Field(default=0, ge=0, le=2)
    user_id: int


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    completed: bool
    priority: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)


class TaskUpdate(BaseModel):
    title: str
    description: str
    completed: bool
    priority: int = Field(ge=0, le=2)


@app.post("/tasks", response_model=TaskResponse)
def create_task(task: TaskCreate, db=Depends(get_db)):
    
    usuario = db.get(User, task.user_id)

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    nova_tarefa = Task(
        title=task.title,
        description=task.description,
        completed=False,
        priority=task.priority,
        user_id=task.user_id
    )

    db.add(nova_tarefa)

    try:
        db.commit()
        db.refresh(nova_tarefa)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Erro de integridade dos dados"
        )
    
    return nova_tarefa

@app.get("/tasks", response_model=list[TaskResponse])
def get_tasks(
    limit: int = Query(5, ge=1, le=100), 
    offset: int = Query(0, ge=0), 
    completed: bool | None=None, 
    title: str | None = None,
    db=Depends(get_db)
):

    stmt = select(Task)#.order_by(Task.id).offset(offset).limit(limit)

    if completed is not None:
        stmt = stmt.where(Task.completed == completed)
    
    if title is not None:
        stmt = stmt.where(Task.title == title)
    
    stmt = stmt.order_by(Task.id)

    stmt = stmt.order_by(Task.id)
    stmt = stmt.offset(offset)
    stmt = stmt.limit(limit)

    result = db.execute(stmt)
    tarefas = result.scalars().all()

    return tarefas


@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db=Depends(get_db)):
    tarefa = db.get(Task, task_id)

    if not tarefa:
        raise HTTPException(status_code=404, detail="Task not found")

    return tarefa


@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task: TaskUpdate, task_id: int, db=Depends(get_db)):
    tarefa = db.get(Task, task_id)

    if not tarefa:
        raise HTTPException(status_code=404, detail="Task not found")

    tarefa.title = task.title
    tarefa.description = task.description
    tarefa.completed = task.completed
    tarefa.priority=task.priority

    try:
        db.commit()
        db.refresh(tarefa)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Erro de integridade dos dados"
        )

    return tarefa


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db=Depends(get_db)):
    tarefa = db.get(Task, task_id)

    if not tarefa:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(tarefa)
    db.commit()

    return {"message": "Tarefa removida com sucesso"}

@app.get("/teste-relationship/{task_id}")
def teste_relationship(task_id: int, db=Depends(get_db)):
    tarefa = db.get(Task, task_id)

    return {
        "tarefa": tarefa.title,
        "usuario": tarefa.user.name
    }

@app.get("/users/{user_id}/tasks", response_model=list[TaskResponse])
def get_user_tasks(user_id: int, db=Depends(get_db)):
    usuario=db.get(User, user_id)

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )
    tarefas = usuario.tasks
    return tarefas