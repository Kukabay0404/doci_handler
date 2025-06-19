from datetime import datetime
from docxtpl import DocxTemplate
from docx2pdf import convert
import asyncio
import re
import os
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.doci import Document
from src.schemas.f_docx import DismissalData, VacationData, TransferData, ApplicationData


def sanitize_filename(name : str):
    name = re.sub(r'[^\w\s-]', '', name)
    name = name.strip().replace(' ', '_')
    return name

async def generate_application_document(
    data: ApplicationData,
    db: AsyncSession,
    template_path: str = "templates/application_template.docx"
):
    # Генерация .docx
    doc = DocxTemplate(template_path)
    context = data.model_dump()
    doc.render(context)

    file_name = sanitize_filename(f"{data.full_name}_перевод" + '.docx')
    output_path = os.path.join("documents", file_name)
    doc.save(output_path)

    # Создание записи в базе
    new_doc = Document(
        type="Заявление на трудоустройство",
        file=file_name,
        created_at=datetime.now()
    )
    db.add(new_doc)
    await db.commit()
    await asyncio.sleep(0.1)
    await db.refresh(new_doc)

    return {"file": file_name, "id": new_doc.id}

async def generate_vacation_document(
    data: VacationData,
    db: AsyncSession,
    template_path: str = "templates/vacation_template.docx"
):
    # Подготовка и рендер шаблона
    doc = DocxTemplate(template_path)
    context = data.model_dump()
    doc.render(context)

    file_name = sanitize_filename(f"{data.full_name}_отпускной" + '.docx')
    output_path = os.path.join("documents", file_name)
    os.makedirs("documents", exist_ok=True)  # гарантия, что директория есть
    doc.save(output_path)

    # Добавление в БД
    try:
        new_doc = Document(
            type="Заявление на отпуск",
            file=file_name,
            created_at=datetime.now()
        )
        db.add(new_doc)
        await db.commit()
        await asyncio.sleep(0.1)
        await db.refresh(new_doc)
    except Exception as e:
        await db.rollback()
        raise e

    return {"file": file_name, "id": new_doc.id}


async def generate_dismissal_document_async(
    data: DismissalData,
    db: AsyncSession,
    template_path: str = "templates/dismissal_template.docx"
):
    # Генерация .docx
    doc = DocxTemplate(template_path)
    context = data.model_dump()
    doc.render(context)

    file_name = sanitize_filename(f"{data.full_name}_увольнение" + '.docx')
    output_path = os.path.join("documents", file_name)
    doc.save(output_path)

    # Создание записи в базе
    new_doc = Document(
        type="Заявление на увольнение",
        file=file_name,
        created_at=datetime.now()
    )
    db.add(new_doc)
    await db.commit()
    await asyncio.sleep(0.1)
    await db.refresh(new_doc)

    return {"file": file_name, "id": new_doc.id}


async def generate_transfer_document(
    data: TransferData,
    db: AsyncSession,
    template_path: str = "templates/transfer_template.docx"
):
    # Генерация .docx
    doc = DocxTemplate(template_path)
    context = data.model_dump()
    doc.render(context)

    file_name = sanitize_filename(f"{data.full_name}_перевод" + '.docx')
    output_path = os.path.join("documents", file_name)
    doc.save(output_path)

    # Создание записи в базе
    new_doc = Document(
        type="Заявление на перевод",
        file=file_name,
        created_at=datetime.now()
    )
    db.add(new_doc)
    await db.commit()
    await asyncio.sleep(0.1)
    await db.refresh(new_doc)

    return {"file": file_name, "id": new_doc.id}