from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime
from app.database import Base

def utc_now():
    return datetime.now(timezone.utc)

class ContactMessage(Base):
    __tablename__ = "contact_messages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False, index=True)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utc_now)

    def __repr__(self):
        return f"<ContactMessage(id={self.id}, name='{self.name}', email='{self.email}')>"
