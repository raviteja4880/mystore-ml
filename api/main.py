from fastapi import FastAPI, Query
from model.recommender import (
    recommend_by_product,
    recommend_from_cart,
    recommend_home
)
from api.retrain_api import router as retrain_router

app = FastAPI(title="MyStore ML Recommendation API")


@app.get("/recommend/product/{external_id}")
def product_recommendations(external_id: str):
    return recommend_by_product(external_id)


@app.post("/recommend/cart")
def cart_recommendations(cart_items: list[str]):
    return {"recommendations": recommend_from_cart(cart_items)}


@app.get("/recommend/home")
def home_recommendations(seed: str = Query(...), limit: int = Query(4)):
    return {"recommendations": recommend_home(seed, limit)}

@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(retrain_router)
