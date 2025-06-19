from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from src.database import get_session, init_db
from src.auth.jwt_handler import decode_access_token, SECRET_KEY, ALGORITHM
from src.crud.user import get_user_by_id
from src.models.user import User
from src.crud import user as user_crud

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(
        token : str = Depends(oauth2_scheme),
        db : AsyncSession = Depends(get_session)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Не удалось проверить учетные данные',
        headers={"WWW-Authenticate": "Bearer"}
    )
    user_id = decode_access_token(token)
    if user_id is None:
        raise credentials_exception

    user = await get_user_by_id(int(user_id), db)
    if user is None:
        raise credentials_exception
    return user

async def admin_required(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_session)
):
    payload = decode_access_token(token)
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Невалидный токен")

    user = await user_crud.get_user_by_id(user_id, db)
    if not user or not user.is_admin:
        raise HTTPException(status_code=403, detail="Доступ запрещен: не админ")

    return user

def get_current_admin_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_session)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Невалидный токен")

        user = db.query(User).filter(User.email == email).first()
        if not user or not user.is_admin:
            raise HTTPException(status_code=403, detail="Доступ запрещён")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Невалидный токен")