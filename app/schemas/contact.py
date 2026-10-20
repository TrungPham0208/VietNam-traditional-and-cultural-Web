from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict

class ContactMessageCreate(BaseModel):
    name: str
    email: EmailStr
    message: str

class ContactMessageResponse(ContactMessageCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
