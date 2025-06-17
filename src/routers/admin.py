from fastapi import APIRouter, Request, Depends, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.jwt_handler import decode_access_token
from src.crud import user as user_crud
from src.auth.deps import admin_required, oauth2_scheme  # ⬅️ сделай Depends-проверку is_admin
import os
from src.crud.user import get_token_from_cookie
from src.database import get_session

router = APIRouter(prefix="/admin", tags=["Admin"])
templates = Jinja2Templates(directory="templates")

@router.get('/check')
async def check_admin(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_session)):
    payload = decode_access_token(token)
    user_id = payload.get("sub")
    user = await user_crud.get_user_by_id(user_id, db)
    if not user or not user.is_admin:
        raise HTTPException(status_code=403, detail='Недостаточно прав')
    return {"is_admin": True}

@router.get("/dashboard")
async def admin_panel(
    request: Request,
    token: str = Depends(get_token_from_cookie),
    db: AsyncSession = Depends(get_session)
):
    payload = decode_access_token(token)
    user = await user_crud.get_user_by_id(payload["sub"], db)
    if not user or not user.is_admin:
        raise HTTPException(status_code=403, detail="Недостаточно прав")
    return templates.TemplateResponse("/admin/dashboard.html", {"request": request, "user": user})


@router.post("/upload_template")
async def upload_template(file: UploadFile = File(...), user=Depends(admin_required)):
    if not file.filename.endswith(".docx"):
        raise HTTPException(status_code=400, detail="Только .docx поддерживается")
    with open(f"template/{file.filename}", "wb") as f:
        f.write(file.file.read())
    return RedirectResponse(url="/admin/", status_code=303)


@router.get("/download")
async def download_doc(document_name: str, user=Depends(admin_required)):
    file_path = os.path.join("documents", document_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Файл не найден")
    return FileResponse(
        file_path,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename=document_name
    )
