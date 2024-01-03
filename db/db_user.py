from sqlalchemy.orm.session import Session
from schemas import (
    UserRegisterForDataBase,
    UserRole
)
from db.models import DbUser
from typing import List


def create_user(request: UserRegisterForDataBase, db: Session, commit= True) -> DbUser:

    user = DbUser(
        name= request.name,
        phone_number= request.phone_number,
        email= request.email,
        username= request.username,
        password= request.password,
        role= request.role
    )
    db.add(user)

    if commit:
        db.commit()
        db.refresh(user)
    
    return user


def get_all_users(db:Session) -> List[DbUser]:

    return db.query(DbUser).all()
    

def get_all_users_by_role(role: UserRole, db:Session) -> List[DbUser]:
    
    return db.query(DbUser).filter(DbUser.role == role).all()


def get_user_by_user_id(user_id, db:Session) -> DbUser:
    
    return db.query(DbUser).filter(DbUser.user_id == user_id ).first()


def get_user_by_phone_number(phone_number, db:Session) -> DbUser:
    
    return db.query(DbUser).filter(DbUser.phone_number == phone_number).first()


def get_user_by_email(email, db:Session) -> DbUser:
    
    return db.query(DbUser).filter(DbUser.email == email).first()


def get_user_by_username(username, db:Session) -> DbUser:
    
    return db.query(DbUser).filter(DbUser.username == username ).first()
    

def update_role(user_id, new_role: UserRole, db:Session ,commit= True):

    user = db.query(DbUser).filter(DbUser.user_id == user_id )
    user.update({DbUser.role: new_role})
    if commit:
        db.commit()    

    return True


def update_phone_number(user_id, new_phone_number: str, db:Session ,commit= True):

    user = db.query(DbUser).filter(DbUser.user_id == user_id )
    user.update({DbUser.phone_number: new_phone_number})
    if commit:
        db.commit()    
            
    return True


def update_name(user_id, new_name: str, db:Session ,commit= True):

    user = db.query(DbUser).filter(DbUser.user_id == user_id )
    user.update({DbUser.name: new_name})
    if commit:
        db.commit()    
            
    return True


def update_email(user_id, new_email: str, db:Session ,commit= True):

    user = db.query(DbUser).filter(DbUser.user_id == user_id )
    user.update({DbUser.email: new_email})
    if commit:
        db.commit()    
            
    return True


def update_password(user_id, new_password: str, db:Session ,commit= True):

    user = db.query(DbUser).filter(DbUser.user_id == user_id )
    user.update({DbUser.password: new_password})
    if commit:
        db.commit()    
            
    return True 


def delete_user(user_id, db:Session):

    user = get_user_by_user_id(user_id, db)
    db.delete(user)
    db.commit()

    return True
