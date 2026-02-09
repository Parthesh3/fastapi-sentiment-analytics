from pydantic import BaseModel, Field
from typing import Optional


class ReviewCreate(BaseModel):
    user_name: str
    rating: int = Field(ge=1, le=5)
    review_text: str = Field(min_length=10)


class ReviewUpdate(BaseModel):
    rating: Optional[int] = Field(None, ge=1, le=5)
    review_text: Optional[str] = Field(None, min_length=10)


class ReviewResponse(BaseModel):
    id: int
    user_name: str
    rating: int
    review_text: str
    sentiment_score: float
    sentiment_label: str

    model_config = {"from_attributes": True}
