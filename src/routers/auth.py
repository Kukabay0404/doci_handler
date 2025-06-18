from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import HTMLResponse
from src.schemas.user import UserCreate, UserRead, UserLogin
from src.database import get_session
from src.crud import user as user_crud
from src.auth.hash import verify_password
from src.auth.jwt_handler import create_access_token
from src.utils.templates import templates
from src.auth.deps import admin_required

router = APIRouter(prefix='/auth', tags=['Auth'])

@router.get("/register", response_class=HTMLResponse)
async def get_register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.post('/register', response_model=UserRead)
async def register(user_data : UserCreate, db : AsyncSession = Depends(get_session)):
    existing = await user_crud.get_user_by_email(user_data.email, db)
    if existing:
        raise HTTPException(status_code=400, detail='Email уже зарегистрирован')
    user = await user_crud.create_user(user_data, db)
    return user


@router.get("/login", response_class=HTMLResponse)
async def get_register(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post('/login')
async def login(data: UserLogin, db: AsyncSession = Depends(get_session)):
    user = await user_crud.get_user_by_email(data.email, db)
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail='Неверные email или пароль')
    token = create_access_token({'sub' : str(user.id)})
    return {'access_token' : token, 'token_type' : 'bearer'}

@router.get("/login-admin", response_class=HTMLResponse)
async def get_register(request: Request):
    return templates.TemplateResponse("login-admin.html", {"request": request})

@router.post('/login-admin')
async def login(data: UserLogin, db: AsyncSession = Depends(get_session)):
    user = await user_crud.get_user_by_email(data.email, db)
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail='Неверные email или пароль')

    if not user.is_admin:
        raise HTTPException(status_code=403, detail='Доступ разрешён только администраторам')

    token = create_access_token({'sub' : str(user.id)})
    return {'access_token' : token, 'token_type' : 'bearer'}