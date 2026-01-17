from fastapi import FastAPI
from model.recommender import (
    recommend_by_product,
    recommend_from_cart
)

app = FastAPI(title="MyStore ML Recommendation API")

@app.get("/recommend/product/{external_id}")
def product_recommendations(external_id: str):
    return recommend_by_product(external_id)

@app.post("/recommend/cart")
def cart_recommendations(cart_items: list[str]):
    return {
        "recommendations": recommend_from_cart(cart_items)
    }
