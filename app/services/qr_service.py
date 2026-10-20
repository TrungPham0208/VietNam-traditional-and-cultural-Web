import io
from pathlib import Path
import qrcode
import qrcode.image.svg
from app.config import settings

def get_qr_url(slug: str) -> str:
    """Trả về URL đích của mã QR (qua route rút gọn /c/{slug})"""
    base = settings.BASE_URL.rstrip("/")
    return f"{base}/c/{slug}"

def generate_qr_png_bytes(slug: str, box_size: int = 10, border: int = 2) -> bytes:
    """Tạo mã QR dạng ảnh PNG (in-memory bytes)"""
    url = get_qr_url(slug)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=box_size,
        border=border,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#1F5C3A", back_color="#FFFFFF")
    
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

def generate_qr_svg_str(slug: str, box_size: int = 10) -> str:
    """Tạo mã QR dạng vector SVG (dễ phóng to khi in ấn thẻ 6x9 cm không bị vỡ hạt)"""
    url = get_qr_url(slug)
    factory = qrcode.image.svg.SvgImage
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=box_size,
        border=2,
        image_factory=factory
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image()
    
    buf = io.BytesIO()
    img.save(buf)
    return buf.getvalue().decode("utf-8")

def save_card_qr_files(slug: str) -> tuple[Path, Path]:
    """Lưu đồng thời file PNG và SVG vào thư mục tĩnh static/qr/"""
    png_path = settings.QR_DIR / f"{slug}.png"
    svg_path = settings.QR_DIR / f"{slug}.svg"
    
    # Tạo và lưu PNG
    png_bytes = generate_qr_png_bytes(slug)
    with open(png_path, "wb") as f:
        f.write(png_bytes)
        
    # Tạo và lưu SVG
    svg_str = generate_qr_svg_str(slug)
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg_str)
        
    return png_path, svg_path
