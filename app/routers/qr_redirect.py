from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.card import Card

router = APIRouter(tags=["QR Redirect"])

@router.get("/c/{slug}", summary="Tuyến quét QR ngắn, ghi nhận lượt quét ẩn danh và chuyển hướng 302")
def redirect_qr_scan(slug: str, db: Session = Depends(get_db)):
    """
    Sinh viên quét thẻ vật lý -> Trình duyệt truy cập URL ngắn /c/{slug} -> 
    Hệ thống tự động tăng bộ đếm scan_count cho thẻ -> Redirect 302 sang trang chi tiết /card/{slug}.
    Hoàn toàn ẩn danh, không lưu IP hoặc thông tin cá nhân của người quét.
    """
    card = db.query(Card).filter(Card.slug == slug).first()
    if not card:
        raise HTTPException(status_code=404, detail="Mã thẻ QR không tồn tại trong hệ thống VietTrans.")

    # Tăng số lượt quét
    card.scan_count = (card.scan_count or 0) + 1
    db.commit()

    # Chuyển hướng 302 sang trang chi tiết thẻ
    return RedirectResponse(url=f"/card/{slug}", status_code=status.HTTP_302_FOUND)
