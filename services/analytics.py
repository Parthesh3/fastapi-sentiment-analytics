from sqlalchemy.orm import Session
from models.review import Review
from sqlalchemy import func

def product_analytics(db: Session, product_id: int):
    reviews = db.query(Review).filter(Review.product_id == product_id).all()
    total = len(reviews)

    if total == 0:
        return {}

    avg_rating = sum(r.rating for r in reviews) / total
    avg_sentiment = sum(r.sentiment_score for r in reviews) / total

    sentiment_counts = {
        "positive": len([r for r in reviews if r.sentiment_label == "positive"]),
        "negative": len([r for r in reviews if r.sentiment_label == "negative"]),
        "neutral": len([r for r in reviews if r.sentiment_label == "neutral"]),
    }

    return {
        "total_reviews": total,
        "average_rating": round(avg_rating, 2),
        "average_sentiment_score": round(avg_sentiment, 3),
        "sentiment_distribution": {
            k: round(v * 100 / total, 2) for k, v in sentiment_counts.items()
        },
        "most_positive_review": max(reviews, key=lambda r: r.sentiment_score).review_text,
        "most_negative_review": min(reviews, key=lambda r: r.sentiment_score).review_text,
    }


def get_product_analytics(db: Session, product_id: int):
    reviews = db.query(Review).filter(Review.product_id == product_id).all()

    total_reviews = len(reviews)

    if total_reviews == 0:
        return {
            "total_reviews": 0,
            "average_rating": 0,
            "average_sentiment_score": 0,
            "sentiment_distribution": {
                "positive": 0,
                "neutral": 0,
                "negative": 0
            },
            "most_positive_review": None,
            "most_negative_review": None
        }

    avg_rating = sum(r.rating for r in reviews) / total_reviews
    avg_sentiment = sum(r.sentiment_score for r in reviews) / total_reviews

    positives = [r for r in reviews if r.sentiment_label == "positive"]
    negatives = [r for r in reviews if r.sentiment_label == "negative"]
    neutrals = [r for r in reviews if r.sentiment_label == "neutral"]

    return {
        "total_reviews": total_reviews,
        "average_rating": round(avg_rating, 2),
        "average_sentiment_score": round(avg_sentiment, 3),
        "sentiment_distribution": {
            "positive": round(len(positives) * 100 / total_reviews, 2),
            "neutral": round(len(neutrals) * 100 / total_reviews, 2),
            "negative": round(len(negatives) * 100 / total_reviews, 2),
        },
        "most_positive_review": max(
            reviews, key=lambda r: r.sentiment_score
        ).review_text,
        "most_negative_review": min(
            reviews, key=lambda r: r.sentiment_score
        ).review_text,
    }