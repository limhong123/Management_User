from sqlalchemy.orm import Session
import models,schema

def create_user(db:Session,user:schema.UserCreate):
    db_user = models.User_DB(
        name=user.name,
        email=user.email
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_users(db:Session):
    return db.query(models.User_DB).all()


def get_user_byID(db:Session,user_id:int):
    return db.query(models.User_DB).filter(
        models.User_DB.id == user_id
    ).first()


def update_user(db:Session,user_id:int,user:schema.UserUpdate):

    db_user = get_user_byID(db,user_id)

    if not db_user:
        return None

    if user.name is not None:
        db_user.name = user.name

    if user.email is not None:
        db_user.email = user.email

    db.commit()
    db.refresh(db_user)

    return db_user


def delete_user(db:Session,user_id:int):

    db_user = get_user_byID(db,user_id)

    if not db_user:
        return None

    db.delete(db_user)
    db.commit()

    return db_user