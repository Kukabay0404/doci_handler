from fastapi import APIRouter, Request, Depends, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, RedirectResponse
from src.utils.templates import templates
from fastapi.responses import HTMLResponse
from src.auth.deps import admin_required, oauth2_scheme  # ⬅️ сделай Depends-проверку is_admin
import os

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/dashboard", response_class=HTMLResponse)
async def get_register(request: Request):
    return templates.TemplateResponse("admin/dashboard.html", {"request": request})


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
