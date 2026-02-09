# fastapi-sentiment-analytics
Overview

This project is a FastAPI-based backend application that manages products and reviews, performs sentiment analysis on user reviews, and provides analytics insights per product.

The system automatically analyzes review sentiment at creation/update time and exposes analytics APIs for business insights.

# Tech Stack

FastAPI – REST API framework

Python 3.12

SQLAlchemy – ORM

SQLite (can be replaced with PostgreSQL)

Hugging Face Transformers / TextBlob – Sentiment Analysis

Uvicorn – ASGI server

Docker – Containerization

# Features

Product CRUD operations

Review CRUD with automatic sentiment analysis

Rating & input validation

Product-level analytics

Async-ready architecture

Clean modular folder structure


# Setup & Run
# Local Setup
        python -m venv env
        source env/bin/activate   # Windows: env\Scripts\activate
        pip install -r requirements.txt
        uvicorn main:app --reload

# Using Docker
    docker build -t fastapi-sentiment .
    docker run -p 8000:8000 fastapi-sentiment

# API Documentation
Swagger UI:
http://localhost:8000/docs

# Core APIs
    Product APIs

        POST /api/v1/products

        GET /api/v1/products

        GET /api/v1/products/{product_id}

        PUT /api/v1/products/{product_id}

        DELETE /api/v1/products/{product_id}

    Review APIs

        POST /api/v1/products/{product_id}/reviews

        GET /api/v1/products/{product_id}/reviews

        GET /api/v1/reviews/{review_id}

        PUT /api/v1/reviews/{review_id}

        DELETE /api/v1/reviews/{review_id}

    Analytics API

        GET /api/v1/products/{product_id}/analytics

# Sentiment Analysis

Sentiment is calculated using a dedicated service module
Model is loaded once at application startup
Output:
    sentiment_score
    sentiment_label (positive / neutral / negative)
Sentiment is recalculated automatically when review text changes

# Validation

Rating: 1–5 enforced
Review text: minimum 10 characters
Product name: required, max 200 chars
