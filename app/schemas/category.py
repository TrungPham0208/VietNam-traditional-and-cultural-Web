from typing import Optional
from pydantic import BaseModel, ConfigDict

class CategoryBase(BaseModel):
    slug: str
    name_vi: str
    name_en: str
    description: Optional[str] = None
    icon: Optional[str] = None
    expected_cards_min: int = 6
    expected_cards_max: int = 10
    sort_order: int = 0

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    slug: Optional[str] = None
    name_vi: Optional[str] = None
    name_en: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    expected_cards_min: Optional[int] = None
    expected_cards_max: Optional[int] = None
    sort_order: Optional[int] = None

class CategoryResponse(CategoryBase):
    id: int
    card_count: Optional[int] = 0

    model_config = ConfigDict(from_attributes=True)
