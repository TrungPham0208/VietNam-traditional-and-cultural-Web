from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import qr_redirect, pages, api

app = FastAPI(
    title=settings.APP_TITLE,
    description="Hệ thống bộ thẻ QR hỗ trợ biên dịch các yếu tố văn hóa Việt Nam sang tiếng Anh",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Phục vụ file tĩnh (CSS, JS, Ảnh, Mã QR, Âm thanh)
app.mount("/static", StaticFiles(directory=str(settings.STATIC_DIR)), name="static")

templates = Jinja2Templates(directory=str(settings.TEMPLATES_DIR))

# Đăng ký các router
app.include_router(qr_redirect.router)
app.include_router(pages.router)
app.include_router(api.router)

@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return templates.TemplateResponse(
        request=request,
        name="404.html",
        context={"settings": settings},
        status_code=404
    )
