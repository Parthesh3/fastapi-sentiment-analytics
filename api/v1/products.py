from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from fastapi.concurrency import run_in_threadpool

from core.database import SessionLocal
from models.product import Product
from models.review import Review
from schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    ProductDetailResponse,
)
from services.analytics import get_product_analytics
from schemas.analytics import ProductAnalyticsResponse

router = APIRouter(
    prefix="/api/v1/products",
    tags=["Products"]
)


# ------------------ DB Dependency ------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ------------------ CREATE PRODUCT ------------------
@router.post("", response_model=ProductResponse, status_code=201)
async def create_product(
    payload: ProductCreate,
    db: Session = Depends(get_db)
):
    product = Product(**payload.model_dump())

    await run_in_threadpool(db.add, product)
    await run_in_threadpool(db.commit)
    await run_in_threadpool(db.refresh, product)

    return product


# ------------------ LIST PRODUCTS ------------------
@router.get("", response_model=List[ProductResponse])
async def list_products(
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100),
    category: Optional[str] = None,
    db: Session = Depends(get_db),
):
    def query_products():
        query = db.query(Product)
        if category:
            query = query.filter(Product.category == category)

        return (
            query
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )

    return await run_in_threadpool(query_products)


# ------------------ GET PRODUCT BY ID ------------------
@router.get("/{product_id}", response_model=ProductDetailResponse)
async def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = await run_in_threadpool(db.get, Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    reviews = await run_in_threadpool(lambda: product.reviews)
    total_reviews = len(reviews)

    avg_rating = (
        sum(r.rating for r in reviews) / total_reviews
        if total_reviews > 0 else 0
    )

    return {
        **product.__dict__,
        "total_reviews": total_reviews,
        "average_rating": round(avg_rating, 2),
    }


# ------------------ UPDATE PRODUCT ------------------
@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    payload: ProductUpdate,
    db: Session = Depends(get_db),
):
    product = await run_in_threadpool(db.get, Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(product, field, value)

    await run_in_threadpool(db.commit)
    await run_in_threadpool(db.refresh, product)

    return product


# ------------------ DELETE PRODUCT ------------------
@router.delete("/{product_id}", status_code=204)
async def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = await run_in_threadpool(db.get, Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    await run_in_threadpool(db.delete, product)
    await run_in_threadpool(db.commit)


# ------------------ PRODUCT ANALYTICS ------------------
@router.get(
    "/{product_id}/analytics",
    response_model=ProductAnalyticsResponse
)
async def product_analytics(
    product_id: int,
    db: Session = Depends(get_db),
):
    product = await run_in_threadpool(db.get, Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return await run_in_threadpool(get_product_analytics, db, product_id)
