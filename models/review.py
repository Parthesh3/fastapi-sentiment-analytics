from sqlalchemy import (
    Column, Integer, String, Text, Float,
    ForeignKey, DateTime
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from core.database import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    user_name = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)
    review_text = Column(Text, nullable=False)
    sentiment_score = Column(Float)
    sentiment_label = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    product = relationship("Product", back_populates="reviews")
