from fastapi import APIRouter, Request, BackgroundTasks, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.deps import get_current_user
from src.database import get_session
from src.models.user import User
from src.schemas.f_docx import ApplicationData, VacationData, DismissalData, TransferData
from src.crud.f_docx import (generate_application_document, generate_vacation_document,
                             generate_transfer_document, generate_dismissal_document_async)
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
async def generate_doc(
    data: ApplicationData,
    db: AsyncSession = Depends(get_session),
):
    return await generate_application_document(data, db)


@doc_router.get("/vacation-form", response_class=HTMLResponse)
async def get_application_form(request: Request):
    return templates.TemplateResponse("forms/form_vacation.html", {"request": request})

@doc_router.post('/vacation-form')
async def generate_doc(
    data: VacationData,
    db: AsyncSession = Depends(get_session),
):
    return await generate_vacation_document(data, db)


@doc_router.get("/dismissal-form", response_class=HTMLResponse)
async def get_application_form(request: Request):
    return templates.TemplateResponse("forms/dismissal_form.html", {"request": request})

@doc_router.post('/dismissal-form')
async def create_dismissal_document(
    data: DismissalData,
    db: AsyncSession = Depends(get_session),
):
    return await generate_dismissal_document_async(data, db)


@doc_router.get("/transfer-form", response_class=HTMLResponse)
async def get_application_form(request: Request):
    return templates.TemplateResponse("forms/transfer_form.html", {"request": request})

@doc_router.post('/transfer-form')
async def generate_doc(
    data: TransferData,
    db: AsyncSession = Depends(get_session),
):
    return await generate_transfer_document(data, db)
