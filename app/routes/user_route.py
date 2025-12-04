from fastapi import APIRouter, Depends, Request, HTTPException, status
from app.models.user import User
from app.schemas.user_schema import UserCreateRequest, UserUpdateRequest, User as UserResponse 
from app.database import SessionDep
from ..middleware.auth import AuthMiddleware
from datetime import datetime
from typing import List
import logging
import pymysql
import bcrypt

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create(user_request: UserCreateRequest, db: SessionDep, request: Request):

    user_exists = db.query(User).filter(
        (user_request.email == User.email) | (user_request.phone == User.phone)
    ).first()

    if user_exists: 
        raiseError("email or phone already exists", request)
    
    salts = bcrypt.gensalt(rounds=12)
    hashed_password = bcrypt.hashpw(user_request.password.encode('utf-8'), salts)
    
    new_user = User(
        **user_request.dict(exclude={"password", "confirm_password"}),
        password=hashed_password.decode(),
    )

    try:  
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user
    except pymysql.DataError as e:
        raiseError(e, request)
    except Exception as e:
        raiseError(e, request)

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[UserResponse])
def get_all_users(db: SessionDep, request: Request):
    users = db.query(User).all()

    if not users:
        raiseError("No available users", request)

    return users

@router.get("/me", status_code=status.HTTP_200_OK)
def get_current_user(current_user = Depends(AuthMiddleware)):
    return current_user


@router.put("/", status_code=status.HTTP_200_OK, response_model=UserResponse)
def update_user(user_request: UserUpdateRequest, db: SessionDep, request: Request, current_user = Depends(AuthMiddleware)):

    update_data = user_request.dict(exclude_unset=True)

    try:
        for field, value in update_data.items():
            setattr(current_user, field, value)
        db.commit()
        db.refresh(current_user)
        return current_user
    except pymysql.DataError as e:
        raiseError(e, request)
    except Exception as e:
        raiseError(e, request)


@router.delete("/", status_code=status.HTTP_200_OK, response_model=UserResponse)
def delete_user(db: SessionDep, request: Request, current_user = Depends(AuthMiddleware)):
    user = db.query(User).filter(User.id == current_user.id).first()
    deleted_user = user
    try:
        db.delete(user)
        db.commit()

        return deleted_user 
    except pymysql.DataError as e:
        raiseError(e, request)
    except Exception as e:
        raiseError(e, request)


def raiseError(e: str, request: Request):
 
    method = request.method.upper()

    if method == "POST":
        message = f"Failed to create record: {e}"
    elif method == "GET":
        message = f"Failed to fetch record: {e}"
    elif method in ("PUT", "PATCH"):
        message = f"Failed to update record: {e}"
    elif method == "DELETE":
        message = f"Failed to delete record: {e}"
    else:
        message = f"Error: {e}"

    logger.error(message)
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail={
            "status": "error",
            "message": message,
            "timestamp": datetime.utcnow().isoformat()
        }
    )
