import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class RecommendationService:

    def recommend(self):

        user_vector = np.array([[0.8, 0.2, 0.9]])

        item_vectors = np.array([
            [0.7, 0.1, 0.8],
            [0.2, 0.9, 0.1],
            [0.9, 0.2, 0.95]
        ])

        scores = cosine_similarity(user_vector, item_vectors)[0]

        ranked = np.argsort(scores)[::-1]

        return {
            "recommendations": ranked.tolist(),
            "scores": scores.tolist()
        }