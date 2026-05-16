from sqlalchemy.orm import Session
from database import SessionLocal
from fastapi import APIRouter,Depends,HTTPException
import crud 
from schema import UserCreate,UserResponse,UserUpdate

router = APIRouter()


@router.post("/users/",response_model=UserResponse)
def create_user(user:UserCreate,db:Session=Depends(get_db)):
    return crud.create_user(db,user)