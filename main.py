from fastapi import FastAPI
from core.database import Base, engine
from api.v1 import products, reviews, analysis

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Product Review Sentiment API")

app.include_router(products.router)
app.include_router(reviews.router)
app.include_router(analysis.router)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)