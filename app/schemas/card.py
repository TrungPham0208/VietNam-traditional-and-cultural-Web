from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class CardExampleSchema(BaseModel):
    id: Optional[int] = None
    sentence_vi: str
    sentence_en: str
    sort_order: int = 0

    model_config = ConfigDict(from_attributes=True)


class PracticeItemSchema(BaseModel):
    id: Optional[int] = None
    prompt: str
    suggested_answer: str
    hint: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class CardBase(BaseModel):
    slug: str
    term_vi: str
    category_id: int
    category_label: Optional[str] = None
    tagline_en: Optional[str] = None
    suggested_translation: str
    meaning: str
    cultural_note: str
    translation_strategy: str
    common_mistake: Optional[str] = None
    translation_tip: Optional[str] = None
    image_path: Optional[str] = None
    audio_path: Optional[str] = None
    status: str = "published"
    reviewed: bool = False


class CardCreate(CardBase):
    examples: List[CardExampleSchema] = []
    practice_items: List[PracticeItemSchema] = []


class CardUpdate(BaseModel):
    slug: Optional[str] = None
    term_vi: Optional[str] = None
    category_id: Optional[int] = None
    category_label: Optional[str] = None
    tagline_en: Optional[str] = None
    suggested_translation: Optional[str] = None
    meaning: Optional[str] = None
    cultural_note: Optional[str] = None
    translation_strategy: Optional[str] = None
    common_mistake: Optional[str] = None
    translation_tip: Optional[str] = None
    image_path: Optional[str] = None
    audio_path: Optional[str] = None
    status: Optional[str] = None
    reviewed: Optional[bool] = None
    examples: Optional[List[CardExampleSchema]] = None
    practice_items: Optional[List[PracticeItemSchema]] = None


class CardResponse(CardBase):
    id: int
    scan_count: int
    created_at: datetime
    updated_at: datetime
    examples: List[CardExampleSchema] = []
    practice_items: List[PracticeItemSchema] = []

    model_config = ConfigDict(from_attributes=True)


class CardSummaryResponse(BaseModel):
    id: int
    slug: str
    term_vi: str
    category_id: int
    category_label: Optional[str] = None
    tagline_en: Optional[str] = None
    suggested_translation: str
    image_path: Optional[str] = None
    status: str
    reviewed: bool
    scan_count: int

    model_config = ConfigDict(from_attributes=True)
