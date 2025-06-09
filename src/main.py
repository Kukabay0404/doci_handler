from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from src.utils.templates import templates
from fastapi.responses import HTMLResponse
from src.routers import auth
from src.routers import users
from src.routers import fw_docx
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title='Электронный документ хэндлер')

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*']
)

app.include_router(fw_docx.doc_router)
app.include_router(auth.router)
app.include_router(users.router)

@app.get('/', response_class=HTMLResponse)
async def read_index(request : Request):
    return templates.TemplateResponse('index.html', {'request' : request})


