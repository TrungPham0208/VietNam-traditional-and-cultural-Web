from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.category import Category
from app.models.card import Card
from app.models.contact import ContactMessage
from app.schemas.category import CategoryResponse
from app.schemas.card import CardResponse, CardSummaryResponse
from app.schemas.contact import ContactMessageCreate, ContactMessageResponse
from app.services.qr_service import generate_qr_png_bytes, generate_qr_svg_str
from app.services.search_service import normalize_text, match_card_query

router = APIRouter(prefix="/api", tags=["Public API"])

@router.get("/categories", response_model=List[CategoryResponse], summary="Lấy danh sách các nhóm văn hóa")
def get_categories(db: Session = Depends(get_db)):
    """Trả về 5 nhóm văn hóa kèm số lượng thẻ của mỗi nhóm"""
    cats = db.query(Category).order_by(Category.sort_order).all()
    results = []
    for cat in cats:
        count = db.query(func.count(Card.id)).filter(
            Card.category_id == cat.id,
            Card.status == "published"
        ).scalar() or 0
        cat_dict = {
            "id": cat.id,
            "slug": cat.slug,
            "name_vi": cat.name_vi,
            "name_en": cat.name_en,
            "description": cat.description,
            "icon": cat.icon,
            "expected_cards_min": cat.expected_cards_min,
            "expected_cards_max": cat.expected_cards_max,
            "sort_order": cat.sort_order,
            "card_count": count
        }
        results.append(cat_dict)
    return results

@router.get("/cards", summary="Tìm kiếm và lọc thẻ văn hóa")
def get_cards(
    q: Optional[str] = Query(None, description="Từ khóa tìm kiếm (hỗ trợ có dấu và không dấu, ví dụ: 'li xi')"),
    category: Optional[str] = Query(None, description="Slug nhóm văn hóa (ví dụ: 'tet-le-hoi')"),
    page: int = Query(1, ge=1, description="Trang hiện tại"),
    limit: int = Query(20, ge=1, le=100, description="Số thẻ trên mỗi trang"),
    db: Session = Depends(get_db)
):
    """
    Tìm kiếm và lọc thẻ theo nhóm văn hóa, hỗ trợ tìm kiếm không dấu thời gian thực.
    """
    query = db.query(Card).filter(Card.status == "published")
    
    # Lọc theo danh mục nếu có
    if category and category.strip():
        cat = db.query(Category).filter(Category.slug == category.strip()).first()
        if cat:
            query = query.filter(Card.category_id == cat.id)
        else:
            return {"total": 0, "page": page, "limit": limit, "items": []}

    all_cards = query.order_by(Card.id).all()
    
    # Tìm kiếm tiếng Việt không dấu nếu có query 'q'
    if q and q.strip():
        norm_q = normalize_text(q.strip())
        matched_cards = [c for c in all_cards if match_card_query(c, norm_q)]
    else:
        matched_cards = all_cards

    total = len(matched_cards)
    start_idx = (page - 1) * limit
    end_idx = start_idx + limit
    paginated_items = matched_cards[start_idx:end_idx]

    items = []
    for c in paginated_items:
        items.append({
            "id": c.id,
            "slug": c.slug,
            "term_vi": c.term_vi,
            "category_id": c.category_id,
            "category_label": c.category_label,
            "tagline_en": c.tagline_en,
            "suggested_translation": c.suggested_translation,
            "image_path": c.image_path,
            "status": c.status,
            "reviewed": c.reviewed,
            "scan_count": c.scan_count
        })

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": (total + limit - 1) // limit if limit > 0 else 1,
        "items": items
    }

@router.get("/cards/{slug}", response_model=CardResponse, summary="Lấy chi tiết 1 thẻ văn hóa")
def get_card_detail(slug: str, db: Session = Depends(get_db)):
    """Trả về đầy đủ 10 khối thông tin văn hóa, ví dụ và bài luyện tập của thẻ"""
    card = db.query(Card).filter(Card.slug == slug).first()
    if not card:
        raise HTTPException(status_code=404, detail="Không tìm thấy thẻ văn hóa với slug này.")
    return card

@router.get("/cards/{slug}/qr", summary="Sinh và trả về mã QR của thẻ")
def get_card_qr(
    slug: str,
    format: str = Query("png", pattern="^(png|svg)$", description="Định dạng mã QR (png hoặc svg)"),
    db: Session = Depends(get_db)
):
    """
    Sinh trực tiếp mã QR trỏ tới URL quét ngắn /c/{slug}.
    Hỗ trợ trả về PNG (cho web) và SVG (cho in ấn chất lượng cao).
    """
    card = db.query(Card).filter(Card.slug == slug).first()
    if not card:
        raise HTTPException(status_code=404, detail="Không tìm thấy thẻ văn hóa.")

    if format == "svg":
        svg_content = generate_qr_svg_str(slug)
        return Response(content=svg_content, media_type="image/svg+xml")
    else:
        png_bytes = generate_qr_png_bytes(slug)
        return Response(content=png_bytes, media_type="image/png")

@router.post("/contact", response_model=ContactMessageResponse, status_code=status.HTTP_201_CREATED, summary="Gửi tin nhắn liên hệ")
def send_contact_message(msg_in: ContactMessageCreate, db: Session = Depends(get_db)):
    """Lưu tin nhắn từ form liên hệ vào cơ sở dữ liệu"""
    msg = ContactMessage(
        name=msg_in.name.strip(),
        email=msg_in.email.strip().lower(),
        message=msg_in.message.strip()
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg
