from sqlalchemy import select, func
from datetime import date, datetime
from fastapi import APIRouter, Request, Depends, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.jwt_handler import decode_access_token
from src.crud.user import get_token_from_cookie
from src.database import get_session
from src.models.doci import Document
from src.models.user import User
from src.utils.templates import templates
from fastapi.responses import HTMLResponse
from src.auth.deps import admin_required
from src.crud import user as user_crud
import os

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get('/check')
async def get_current_admin(token: str = Depends(get_token_from_cookie), db: AsyncSession = Depends(get_session)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Невалидный токен")

    user = await user_crud.get_user_by_id(payload["sub"], db)
    if not user or not user.is_admin:
        raise HTTPException(status_code=403, detail="Недостаточно прав")

    return user


@router.get("/dashboard", response_class=HTMLResponse)
async def get_register(request: Request, _: dict = Depends(get_current_admin)):
    return templates.TemplateResponse("admin/dashboard.html", {"request": request})


@router.get("/documents-page")
async def get_documents_page(
    request: Request,
    _: dict = Depends(get_current_admin),
):
    return templates.TemplateResponse("admin/incdocuments.html", {"request": request})

@router.get("/templates", response_class=HTMLResponse)
async def get_register(request: Request, _: dict = Depends(get_current_admin)):
    return templates.TemplateResponse("admin/tempshlates.html", {"request": request})

@router.get("/stats")
async def get_dashboard_stats(
    db: AsyncSession = Depends(get_session),
):
    today_start = datetime.combine(date.today(), datetime.min.time())

    # Общее количество пользователей
    total_users_result = await db.execute(select(func.count()).select_from(User))
    total_users = total_users_result.scalar()

    # Общее количество документов
    total_documents_result = await db.execute(select(func.count()).select_from(Document))
    total_documents = total_documents_result.scalar()

    # Документы, созданные сегодня
    today_documents_result = await db.execute(
        select(func.count()).select_from(Document).where(Document.created_at >= today_start)
    )
    today_documents = today_documents_result.scalar()

    # Последние 5 документов
    recent_documents_result = await db.execute(
        select(Document).order_by(Document.created_at.desc()).limit(5)
    )
    recent_documents = recent_documents_result.scalars().all()

    return {
        "total_users": total_users,
        "total_documents": total_documents,
        "today_documents": today_documents,
        "recent_documents": [
            {
                "id": doc.id,
                "type": doc.type,
                "created_at": doc.created_at
            } for doc in recent_documents
        ]
    }






@router.post("/upload_template")
async def upload_template(file: UploadFile = File(...)):
    if not file.filename.endswith(".docx"):
        raise HTTPException(status_code=400, detail="Только .docx поддерживается")
    with open(f"template/{file.filename}", "wb") as f:
        f.write(file.file.read())
    return RedirectResponse(url="/admin/", status_code=303)


@router.get("/download")
async def download_doc(document_name: str):
    file_path = os.path.join("documents", document_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Файл не найден")
    return FileResponse(
        file_path,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename=document_name
    )
