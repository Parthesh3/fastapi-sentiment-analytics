from pydantic import BaseModel
from typing import Optional, Dict


class ProductAnalyticsResponse(BaseModel):
    total_reviews: int
    average_rating: float
    average_sentiment_score: float
    sentiment_distribution: Dict[str, float]
    most_positive_review: Optional[str]
    most_negative_review: Optional[str]
