import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# Đường dẫn thư mục gốc ứng dụng
APP_DIR = Path(__file__).resolve().parent
PROJECT_DIR = APP_DIR.parent

class Settings(BaseSettings):
    APP_ENV: str = "development"
    APP_TITLE: str = "VietTrans - Lan tỏa văn hóa Việt qua ngôn ngữ Anh"
    BASE_URL: str = "http://localhost:8000"
    
    # Cơ sở dữ liệu
    DATABASE_URL: str = "sqlite:///./viettrans.db"
    
    # Tài khoản quản trị & bảo mật phiên
    SECRET_KEY: str = "viettrans-super-secret-key-change-in-production-2026"
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "viettrans_admin_2026"
    ADMIN_SESSION_EXPIRE_HOURS: int = 24
    
    # Đường dẫn thư mục tĩnh & tải lên
    STATIC_DIR: Path = APP_DIR / "static"
    TEMPLATES_DIR: Path = APP_DIR / "templates"
    QR_DIR: Path = APP_DIR / "static" / "qr"
    UPLOAD_DIR: Path = APP_DIR / "static" / "uploads"
    AUDIO_DIR: Path = APP_DIR / "static" / "audio"
    
    model_config = SettingsConfigDict(
        env_file=str(PROJECT_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()

# Đảm bảo các thư mục tài nguyên luôn tồn tại
settings.QR_DIR.mkdir(parents=True, exist_ok=True)
settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
settings.AUDIO_DIR.mkdir(parents=True, exist_ok=True)
