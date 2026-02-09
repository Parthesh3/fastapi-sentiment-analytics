from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ProductCreate(BaseModel):
    name: str = Field(..., max_length=200)
    description: Optional[str] = None
    category: str


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    category: Optional[str] = None


class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    category: str
    created_at: datetime

    model_config = {"from_attributes": True}


class ProductDetailResponse(ProductResponse):
    total_reviews: int
    average_rating: float
