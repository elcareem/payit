from app.database import get_db
from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.models.user import User
from app.auth.jwt import create_access_token
from app.config.oauth import oauth, AUTH0_DOMAIN, AUTH0_CLIENT_ID
import logging
import pymysql


logger = logging.getLogger(__name__)


router = APIRouter(prefix="/oauths", tags=["oauth"])

db_dependency = Annotated[Session, Depends(get_db)]

@router.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for("callback")
    print("==============",redirect_uri)
    try:
        return await oauth.auth0.authorize_redirect(request, redirect_uri = redirect_uri)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail =f"Auth Error: Failed to authenticate user {e}")

@router.get("/callback", name = "callback")
async def callback(request: Request, db: db_dependency):
    try:
        token = await oauth.auth0.authorize_access_token(request)
        user_info=token.get("userinfo")
        print("==============",user_info)
        email = user_info.get('email')
        print("=============",email)
        user = db.query(User).filter(User.email == email).first()

        if not user:
            user = User(
                name=user_info['name'],
                email=email
            )
            db.add(user)
            db.commit()
            db.refresh(user)

        jwt = create_access_token({
            "sub":str(user.id),
            "email":user.email,
            "user_id":str(user.id)
        })

        return{
            "access token":jwt,
            "email":user.email,
            "user_id":user.id
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Auth Error: Failed to generate token {e}")
    except pymysql.DataError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail =f"Database Error: {e}")

@router.get("/logout")
def logout(request: Request):
    return_url = "http://localhost:8000"
    logout_url = (
        f"https://{AUTH0_DOMAIN}/v2/logout?"
        f"client_id={AUTH0_CLIENT_ID}&"
        f"returnTo={return_url}"
    )

    return RedirectResponse(url=logout_url)