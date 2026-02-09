
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from fastapi.concurrency import run_in_threadpool

from core.database import SessionLocal
from models.review import Review
from models.product import Product
from schemas.review import ReviewCreate, ReviewUpdate, ReviewResponse
from services.sentiment import sentiment_service

router = APIRouter(prefix="/api/v1", tags=["Reviews"])


# ------------------ DB Dependency ------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ------------------ CREATE REVIEW ------------------
@router.post(
    "/products/{product_id}/reviews",
    response_model=ReviewResponse,
    status_code=201
)
async def create_review(
    product_id: int,
    payload: ReviewCreate,
    db: Session = Depends(get_db),
):
    product = await run_in_threadpool(db.get, Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    sentiment = await sentiment_service.analyze(payload.review_text)

    review = Review(
        product_id=product_id,
        user_name=payload.user_name,
        rating=payload.rating,
        review_text=payload.review_text,
        **sentiment
    )

    await run_in_threadpool(db.add, review)
    await run_in_threadpool(db.commit)
    await run_in_threadpool(db.refresh, review)

    return review


# ------------------ LIST REVIEWS ------------------
@router.get(
    "/products/{product_id}/reviews",
    response_model=List[ReviewResponse]
)
async def list_reviews(
    product_id: int,
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100),
    sentiment: Optional[str] = Query(None, regex="^(positive|negative|neutral)$"),
    db: Session = Depends(get_db),
):
    product = await run_in_threadpool(db.get, Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    def query_reviews():
        query = db.query(Review).filter(Review.product_id == product_id)
        if sentiment:
            query = query.filter(Review.sentiment_label == sentiment)
        return (
            query
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )

    return await run_in_threadpool(query_reviews)


# ------------------ GET REVIEW BY ID ------------------
@router.get(
    "/reviews/{review_id}",
    response_model=ReviewResponse
)
async def get_review(review_id: int, db: Session = Depends(get_db)):
    review = await run_in_threadpool(db.get, Review, review_id)

    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    return review


# ------------------ UPDATE REVIEW ------------------
@router.put(
    "/reviews/{review_id}",
    response_model=ReviewResponse
)
async def update_review(
    review_id: int,
    payload: ReviewUpdate,
    db: Session = Depends(get_db),
):
    review = await run_in_threadpool(db.get, Review, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    if payload.review_text:
        sentiment = await sentiment_service.analyze(payload.review_text)
        review.review_text = payload.review_text
        review.sentiment_score = sentiment["sentiment_score"]
        review.sentiment_label = sentiment["sentiment_label"]

    if payload.rating is not None:
        review.rating = payload.rating

    await run_in_threadpool(db.commit)
    await run_in_threadpool(db.refresh, review)

    return review


# ------------------ DELETE REVIEW ------------------
@router.delete(
    "/reviews/{review_id}",
    status_code=204
)
async def delete_review(review_id: int, db: Session = Depends(get_db)):
    review = await run_in_threadpool(db.get, Review, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    await run_in_threadpool(db.delete, review)
    await run_in_threadpool(db.commit)
