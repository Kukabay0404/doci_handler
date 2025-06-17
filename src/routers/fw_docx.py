from fastapi import APIRouter, UploadFile, File, HTTPException, Request, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.responses import HTMLResponse

from src.schemas.f_docx import ApplicationData, VacationData, DismissalData, TransferData
from src.crud.f_docx import (generate_application_document, generate_vacation_document, generate_dismissal_document,
                             generate_transfer_document)
import os
from src.utils.templates import templates

doc_router = APIRouter(
    prefix='/forms',
    tags=['Documents']
)

@doc_router.get("/manual_forms", response_class=HTMLResponse)
async def get_manual_forms(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@doc_router.get("/application_document", response_class=HTMLResponse)
async def get_application_form(request: Request):
    return templates.TemplateResponse("forms/application_form.html", {"request": request})

@doc_router.post('/job-application')
def generate_doc(data : ApplicationData, background_task : BackgroundTasks):
    background_task.add_task(generate_application_document, data.model_dump(), 'templates/application_template.docx')
    return {'document generated' : 'Документ создан, посмотри'}


@doc_router.get("/vacation-form", response_class=HTMLResponse)
async def get_application_form(request: Request):
    return templates.TemplateResponse("forms/form_vacation.html", {"request": request})

@doc_router.post('/vacation-form')
def generate_doc(data : VacationData):
    file_name = generate_vacation_document(data.model_dump())
    return {'document generated' : file_name}


@doc_router.get("/dismissal-form", response_class=HTMLResponse)
async def get_application_form(request: Request):
    return templates.TemplateResponse("forms/dismissal_form.html", {"request": request})

@doc_router.post('/dismissal-form')
def generate_doc(data : DismissalData):
    file_name = generate_dismissal_document(data.model_dump())
    return {'document generated' : file_name}


@doc_router.get("/transfer-form", response_class=HTMLResponse)
async def get_application_form(request: Request):
    return templates.TemplateResponse("forms/transfer_form.html", {"request": request})

@doc_router.post('/transfer-form')
def generate_doc(data : TransferData):
    file_name = generate_transfer_document(data.model_dump())
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