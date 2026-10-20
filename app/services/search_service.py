import re
from unidecode import unidecode

def normalize_text(text: str) -> str:
    """
    Chuẩn hóa văn bản tiếng Việt sang chữ thường, không dấu, bỏ ký tự thừa.
    Ví dụ: 'Lì xì!' -> 'li xi'
    """
    if not text:
        return ""
    # Chuyển về không dấu
    clean = unidecode(text).lower()
    # Chỉ giữ chữ cái và số
    clean = re.sub(r"[^a-z0-9\s]", " ", clean)
    return " ".join(clean.split())

def match_card_query(card, query_norm: str) -> bool:
    """
    Kiểm tra xem thẻ có khớp với từ khóa tìm kiếm (đã chuẩn hóa) hay không.
    Tìm kiếm trên: Từ tiếng Việt, Gợi ý dịch tiếng Anh, Nghĩa, Ghi chú văn hóa, Nhãn danh mục.
    """
    if not query_norm:
        return True
        
    targets = [
        normalize_text(card.term_vi),
        normalize_text(card.suggested_translation),
        normalize_text(card.tagline_en or ""),
        normalize_text(card.category_label or ""),
        normalize_text(card.meaning or ""),
        normalize_text(card.translation_strategy or "")
    ]
    
    combined = " ".join(targets)
    # Tìm kiếm theo từng từ khóa (AND logic)
    words = query_norm.split()
    return all(word in combined for word in words)
