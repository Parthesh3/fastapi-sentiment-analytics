from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from core.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    category = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    reviews = relationship(
        "Review",
        back_populates="product",
        cascade="all, delete"
    )
