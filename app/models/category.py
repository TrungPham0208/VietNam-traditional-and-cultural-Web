from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.database import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(100), unique=True, index=True, nullable=False)
    name_vi = Column(String(150), nullable=False)
    name_en = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    icon = Column(String(50), nullable=True)  # vd: 'fa-calendar-alt', 'lotus', hoặc tên SVG icon
    expected_cards_min = Column(Integer, default=6)
    expected_cards_max = Column(Integer, default=10)
    sort_order = Column(Integer, default=0)

    # Quan hệ với bảng Card
    cards = relationship("Card", back_populates="category", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Category(id={self.id}, slug='{self.slug}', name_vi='{self.name_vi}')>"
