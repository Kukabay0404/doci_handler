from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models.user import User
from src.schemas.user import UserCreate, CreateAdmin
from src.auth.hash import hash_password
from fastapi import Cookie, HTTPException


async def get_user_by_email(email : str, db : AsyncSession):
    result = await db.execute(select(User).where(User.email == email))
    return result.scalars().first()

async def create_user(user : UserCreate, db : AsyncSession):
    db_user = User(
        email=user.email,
        hashed_password=hash_password(user.password)
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def get_user_by_id(user_id : int, db : AsyncSession):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalars().first()

async def get_token_from_cookie(access_token: str = Cookie(None)):
    if not access_token:
        raise HTTPException(status_code=401, detail="Token missing")
    return access_token
