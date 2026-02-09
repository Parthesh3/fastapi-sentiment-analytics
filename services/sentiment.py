from transformers import pipeline
from fastapi.concurrency import run_in_threadpool
import logging

class SentimentService:
    def __init__(self):
        try:
            self.model = pipeline(
                "sentiment-analysis",
                model="distilbert-base-uncased-finetuned-sst-2-english"
            )
        except Exception as e:
            logging.error(f"Model load failed: {e}")
            self.model = None

    async def analyze(self, text: str) -> dict:
        if not self.model:
            return {
                "sentiment_score": 0.0,
                "sentiment_label": "neutral"
            }

        try:
            result = await run_in_threadpool(self.model, text)
            label = result[0]["label"]
            score = result[0]["score"]

            return {
                "sentiment_score": score if label == "POSITIVE" else -score,
                "sentiment_label": label.lower()
            }
        except Exception:
            return {
                "sentiment_score": 0.0,
                "sentiment_label": "neutral"
            }

sentiment_service = SentimentService()
