import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from load_products import load_products

products = load_products()

products["features"] = (
    (products["name"] + " ") * 2 +
    (products["brand"] + " ") * 2 +
    products["category"] + " " +
    products["description"]
)

tfidf = TfidfVectorizer(stop_words="english")
tfidf_matrix = tfidf.fit_transform(products["features"])

similarity_matrix = cosine_similarity(tfidf_matrix)

with open("recommender.pkl", "wb") as f:
    pickle.dump((products, tfidf, similarity_matrix), f)

print("✅ ML model trained using MongoDB products")
