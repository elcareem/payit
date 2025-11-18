from fastapi import APIRouter, HTTPException, status
from app.models.user import User, UserCreate, UserResponse
from app.database import SessionDep


import bcrypt


router = APIRouter()

@router.post("/users")
def create_user(user: UserCreate, session: SessionDep):
    existing_user = session.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists"
        )
    salt = bcrypt.gensalt(rounds=12)
    password = user.password.encode('utf-8')
    user.password = f"{bcrypt.hashpw(password, salt)}"
    db_user = User(**user.model_dump())
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


