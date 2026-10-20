from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

def utc_now():
    return datetime.now(timezone.utc)

class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(120), unique=True, index=True, nullable=False)
    term_vi = Column(String(150), nullable=False, index=True)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    category_label = Column(String(100), nullable=True)  # vd: "Tết – Lễ hội"
    tagline_en = Column(String(200), nullable=True)     # vd: "Small tradition, Big meaning"
    
    # 10 mục nội dung văn hóa & dịch thuật
    suggested_translation = Column(String(255), nullable=False)
    meaning = Column(Text, nullable=False)
    cultural_note = Column(Text, nullable=False)
    translation_strategy = Column(Text, nullable=False)
    common_mistake = Column(String(255), nullable=True)
    translation_tip = Column(String(255), nullable=True)
    
    # Phương tiện
    image_path = Column(String(255), nullable=True)
    audio_path = Column(String(255), nullable=True)
    
    # Trạng thái & thống kê
    status = Column(String(20), default="published", index=True)  # draft / published
    scan_count = Column(Integer, default=0)
    reviewed = Column(Boolean, default=False)  # Đã được giảng viên duyệt nội dung
    
    created_at = Column(DateTime(timezone=True), default=utc_now)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)

    # Quan hệ
    category = relationship("Category", back_populates="cards")
    examples = relationship("CardExample", back_populates="card", cascade="all, delete-orphan", order_by="CardExample.sort_order")
    practice_items = relationship("PracticeItem", back_populates="card", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Card(id={self.id}, slug='{self.slug}', term_vi='{self.term_vi}', status='{self.status}')>"


class CardExample(Base):
    __tablename__ = "card_examples"

    id = Column(Integer, primary_key=True, index=True)
    card_id = Column(Integer, ForeignKey("cards.id", ondelete="CASCADE"), nullable=False)
    sentence_vi = Column(Text, nullable=False)
    sentence_en = Column(Text, nullable=False)
    sort_order = Column(Integer, default=0)

    card = relationship("Card", back_populates="examples")

    def __repr__(self):
        return f"<CardExample(id={self.id}, card_id={self.card_id})>"


class PracticeItem(Base):
    __tablename__ = "practice_items"

    id = Column(Integer, primary_key=True, index=True)
    card_id = Column(Integer, ForeignKey("cards.id", ondelete="CASCADE"), nullable=False)
    prompt = Column(Text, nullable=False)              # Câu tiếng Việt cần dịch
    suggested_answer = Column(Text, nullable=False)    # Đáp án gợi ý tiếng Anh
    hint = Column(Text, nullable=True)                 # Gợi ý từ vựng / cấu trúc

    card = relationship("Card", back_populates="practice_items")

    def __repr__(self):
        return f"<PracticeItem(id={self.id}, card_id={self.card_id})>"
