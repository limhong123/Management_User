from fastapi import FastAPI,Request,Form,Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import models
import schema
import crud

from database import engine,SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="templates")


# Database Dependency
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# Home Page
@app.get("/")
def home(request: Request, db: Session = Depends(get_db)):

    users = crud.get_users(db)

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"users": users}
    )

# Create User
@app.post("/create")
def create_user(
    name:str = Form(...),
    email:str = Form(...),
    db:Session = Depends(get_db)
):

    user = schema.UserCreate(
        name=name,
        email=email
    )

    crud.create_user(db,user)

    return RedirectResponse("/",status_code=303)


# Edit Page
@app.get("/edit/{user_id}")
def edit_page(
    request: Request,
    user_id: int,
    db: Session = Depends(get_db)
):

    user = crud.get_user_byID(db, user_id)

    return templates.TemplateResponse(
        request=request,
        name="edit.html",
        context={"user": user}
    )

# Update User
@app.post("/update/{user_id}")
def update_user(
    user_id:int,
    name:str = Form(...),
    email:str = Form(...),
    db:Session = Depends(get_db)
):

    user = schema.UserUpdate(
        name=name,
        email=email
    )

    crud.update_user(db,user_id,user)

    return RedirectResponse("/",status_code=303)


# Delete User
@app.post("/delete/{user_id}")
def delete_user(
    user_id:int,
    db:Session = Depends(get_db)
):

    crud.delete_user(db,user_id)

    return RedirectResponse("/",status_code=303)