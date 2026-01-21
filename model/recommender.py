import pickle
import numpy as np

# ===============================
# Load trained model
# ===============================
with open("recommender.pkl", "rb") as f:
    products, tfidf, similarity_matrix = pickle.load(f)

# Map externalId → index
index_map = {
    pid: i for i, pid in enumerate(products["externalId"])
}

# Minimum similarity threshold (important)
MIN_SCORE = 0.05

# ===============================
# Utility: Seeded Shuffle
# ===============================
def seeded_shuffle(items, seed: str):
    hash_val = 0
    for c in seed:
        hash_val = ord(c) + ((hash_val << 5) - hash_val)

    items = items.copy()
    for i in range(len(items) - 1, 0, -1):
        hash_val = (hash_val * 9301 + 49297) % 233280
        j = hash_val % (i + 1)
        items[i], items[j] = items[j], items[i]

    return items

# ===============================
# HOME (USER + DAILY) RECOMMENDATION
# ===============================
def recommend_home(seed: str, top_n=4):
    """
    Deterministic daily recommendations per user.
    Uses seeded shuffle over product corpus.
    """

    if products.empty:
        return []

    # Convert dataframe rows to lightweight dicts
    items = products[["externalId", "name", "brand", "price", "category"]].to_dict("records")

    # Deterministic shuffle
    shuffled = seeded_shuffle(items, seed)

    recommendations = []
    seen_categories = set()

    for product in shuffled:
        # Optional: category diversity (comment out if not needed)
        if product["category"] in seen_categories:
            continue

        recommendations.append({
            "externalId": product["externalId"],
            "name": product["name"],
            "brand": product["brand"],
            "price": int(product["price"]),
            "score": 1.0  # static score for home
        })

        seen_categories.add(product["category"])

        if len(recommendations) == top_n:
            break

    return recommendations

# ===============================
# PRODUCT-BASED RECOMMENDATION
# ===============================
def recommend_by_product(external_id, top_n=4):
    """
    Recommend similar products based on a single product
    """
    if external_id not in index_map:
        return []

    idx = index_map[external_id]
    category = products.iloc[idx]["category"]

    scores = list(enumerate(similarity_matrix[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    recommendations = []

    for i, score in scores:
        if score < MIN_SCORE:
            continue

        product = products.iloc[i]

        if (
            product["category"] == category
            and product["externalId"] != external_id
        ):
            recommendations.append({
                "externalId": product["externalId"],
                "name": product["name"],
                "brand": product["brand"],
                "price": int(product["price"]),
                "score": float(score)
            })

        if len(recommendations) == top_n:
            break

    return recommendations


# ===============================
# CART-BASED RECOMMENDATION
# ===============================
def recommend_from_cart(cart_external_ids, top_n=5):
    """
    Recommend products based on entire cart intent
    """

    valid_indices = [
        index_map[pid]
        for pid in cart_external_ids
        if pid in index_map
    ]

    if not valid_indices:
        return []

    # Find dominant category in cart
    dominant_category = (
        products.iloc[valid_indices]["category"]
        .mode()
        .iloc[0]
    )

    # Aggregate similarity (mean of cart vectors)
    aggregated_scores = np.mean(
        similarity_matrix[valid_indices],
        axis=0
    )

    ranked_indices = aggregated_scores.argsort()[::-1]

    recommendations = []

    for i in ranked_indices:
        score = aggregated_scores[i]

        if score < MIN_SCORE:
            continue

        product = products.iloc[i]

        if (
            product["externalId"] not in cart_external_ids
            and product["category"] == dominant_category
        ):
            recommendations.append({
                "externalId": product["externalId"],
                "name": product["name"],
                "brand": product["brand"],
                "price": int(product["price"]),
                "score": float(score)
            })

        if len(recommendations) == top_n:
            break

    return recommendations
