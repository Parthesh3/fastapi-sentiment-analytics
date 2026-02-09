from fastapi import APIRouter, Body
from services.sentiment import sentiment_service

router = APIRouter(
    prefix="/api/v1",
    tags=["Analysis"]
)

@router.post("/analyze-text")
async def analyze_text(
    text: str = Body(..., min_length=10)
):
    return await sentiment_service.analyze(text)
