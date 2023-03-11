from typing import Optional

from fastapi import FastAPI, Depends, HTTPException
import model
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel,Field


app = FastAPI()

model.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db= SessionLocal()
        yield db
    finally:
        db.close()

class Todo(BaseModel):
    title:str
    description:Optional[str]
    priority:int = Field(gt=0,lt=6,description="the priority must be between 1-5")
    complete:bool


@app.get('/')
async def read_all(db: Session=Depends(get_db)):
    return db.query(model.Todos).all()

@app.get("/todo/{todo_id}")
async def read_todo(todo_id: int,db: Session=Depends(get_db)):
    todo_model = db.query(model.Todos).filter(model.Todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise http_exception()

@app.post("/")
async def create_todo(todo: Todo,db: Session=Depends(get_db)):
    todo_model = model.Todos()
    todo_model.title = todo.title
    todo_model.description = todo_model.description
    todo_model.priority = todo_model.priority
    todo_model.complete = todo_model.complete

    db.add(todo_model)
    db.commit()

    return successful_response(200)


@app.put("/{todo_id}")
async def update_todo(todo_id:int, todo:Todo,db:Session=Depends(get_db)):
    todo_model = db.query(model.Todos).filter(model.Todos.id == todo_id).first()

    if todo_model is None:
        raise http_exception()

    todo_model.title = todo_model.title
    todo_model.description = todo_model.description
    todo_model.priority = todo_model.priority
    todo_model.complete = todo_model.complete

    db.add(todo_model)
    db.commit()


    return successful_response(200)


@app.delete("/{todo_id}")
async def delete_todo(todo_id:int,db:Session=Depends(get_db)):
    todo_model = db.query(model.Todos).filter(model.Todos.id==todo_id).first()

    if todo_model is None:
        raise http_exception()

    db.query(model.Todos).filter(model.Todos.id ==todo_id).delete()
    db.commit()

    return successful_response(200)

def successful_response(status_code:int):
    return
{    'status': 200,
    'transaction': 'successful'
    }
def http_exception():
    return HTTPException(status_code=404,detail="todo not found")
