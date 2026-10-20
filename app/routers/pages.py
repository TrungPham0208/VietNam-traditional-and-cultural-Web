from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models.category import Category
from app.models.card import Card
from app.labels import LABELS

router = APIRouter(tags=["Frontend Pages"])
templates = Jinja2Templates(directory=str(settings.TEMPLATES_DIR))

@router.get("/card/{slug}", response_class=HTMLResponse, summary="Trang chi tiết thẻ quét QR (Mobile-First)")
def card_detail_page(slug: str, request: Request, db: Session = Depends(get_db)):
    """
    Trang chi tiết thẻ - Trang đích khi sinh viên quét mã QR trên thẻ học 6x9 cm.
    Thiết kế mobile-first, hiển thị đầy đủ 10 khối thông tin văn hóa & học thuật.
    """
    card = db.query(Card).filter(Card.slug == slug).first()
    if not card:
        raise HTTPException(status_code=404, detail="Không tìm thấy thẻ văn hóa này.")

    # Tìm thẻ trước và thẻ sau để điều hướng (theo id trong hệ thống)
    prev_card = db.query(Card).filter(Card.id < card.id, Card.status == "published").order_by(Card.id.desc()).first()
    next_card = db.query(Card).filter(Card.id > card.id, Card.status == "published").order_by(Card.id.asc()).first()

    # Tìm các thẻ cùng nhóm văn hóa (tối đa 4 thẻ liên quan)
    related_cards = db.query(Card).filter(
        Card.category_id == card.category_id,
        Card.id != card.id,
        Card.status == "published"
    ).limit(4).all()

    return templates.TemplateResponse(
        request=request,
        name="card_detail.html",
        context={
            "card": card,
            "labels": LABELS,
            "prev_card": prev_card,
            "next_card": next_card,
            "related_cards": related_cards,
            "settings": settings,
        }
    )

@router.get("/", response_class=HTMLResponse, summary="Trang chủ VietTrans")
def home_page(request: Request, db: Session = Depends(get_db)):
    """Trang chủ VietTrans - Tạm thời điều hướng hoặc render index"""
    featured_cards = db.query(Card).filter(Card.status == "published").limit(5).all()
    categories = db.query(Category).order_by(Category.sort_order).all()
    sample_card = db.query(Card).filter(Card.slug == "li-xi").first() or (featured_cards[0] if featured_cards else None)

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "featured_cards": featured_cards,
            "categories": categories,
            "sample_card": sample_card,
            "labels": LABELS,
            "settings": settings
        }
    )

@router.get("/cards", response_class=HTMLResponse, summary="Thư viện thẻ văn hóa")
def cards_library_page(request: Request, db: Session = Depends(get_db)):
    """Trang danh mục thư viện thẻ"""
    categories = db.query(Category).order_by(Category.sort_order).all()
    return templates.TemplateResponse(
        request=request,
        name="cards.html",
        context={
            "categories": categories,
            "labels": LABELS,
            "settings": settings
        }
    )
