from docxtpl import DocxTemplate
from src.schemas.f_docx import ApplicationData
import re
import os

def sanitize_filename(name : str):
    name = re.sub(r'[^\w\s-]', '', name)
    name = name.strip().replace(' ', '_')
    return name

def generate_document(data : dict,  template_path : str = 'templates/application_template.docx'):
    doc = DocxTemplate(template_path)
    doc.render(data)

    full_name = sanitize_filename(data.get('full_name', 'document'))
    file_name = f'{full_name}.docx'
    output_path = os.path.join('documents', file_name)
    doc.save(output_path)

    return {'file' : file_name}
