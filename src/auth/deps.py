from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_session
from src.auth.jwt_handler import decode_access_token
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