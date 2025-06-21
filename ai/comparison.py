from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer('all-MiniLM-L6-v2')

def compare_outlines(actual_outline, ai_outline):
    actual_embedding = model.encode([actual_outline])
    ai_embedding = model.encode([ai_outline])

    similarity = cosine_similarity(actual_embedding, ai_embedding)[0][0]
    return similarity