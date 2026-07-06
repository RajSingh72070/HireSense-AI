from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


model = SentenceTransformer("all-MiniLM-L6-v2")


class SemanticMatcher:

    @staticmethod
    def similarity(job_description, resume_text):

        job_vector = model.encode([job_description])

        resume_vector = model.encode([resume_text])

        similarity = cosine_similarity(
            job_vector,
            resume_vector
        )

        return round(float(similarity[0][0]) * 100, 2)