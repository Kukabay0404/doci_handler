from fastapi import APIRouter, UploadFile, File, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.responses import HTMLResponse
from src.schemas.f_docx import ApplicationData
from src.crud.f_docx import generate_document
import os
from src.utils.templates import templates

doc_router = APIRouter(
    prefix='/docs',
    tags=['Documents']
)

@doc_router.get("/generate", response_class=HTMLResponse)
async def get_register(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@doc_router.post('/generate')
def generate_doc(data : ApplicationData):
    file_name = generate_document(data.model_dump())
    return {'document generated' : file_name}

@doc_router.get('/download/{document_name}')
def download_doc(document_name : str):
    file_path = os.path.join('documents', document_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail='файл не найден')
    return FileResponse(file_path, media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document", filename=document_name)

@doc_router.post('/upload_template')
def upload_template(file : UploadFile = File(...)):
    if not file.filename.endswith('.docx'):
        raise HTTPException(status_code=400, detail='Поддерживаются только .docx файлы')
    with open(f'template/{file.filename}', 'wb') as f:
        f.write(file.file.read())
    return {'message' : "Шаблон успешно загружен"}