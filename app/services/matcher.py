from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class SemanticMatcher:
    _model = None

    @classmethod
    def get_model(cls):
        if cls._model is None:
            cls._model = SentenceTransformer("all-MiniLM-L6-v2")
        return cls._model

    @classmethod
    def similarity(cls, job_description, resume_text):
        model = cls.get_model()

        job_vector = model.encode([job_description])
        resume_vector = model.encode([resume_text])

        score = cosine_similarity(job_vector, resume_vector)

        return round(float(score[0][0]) * 100, 2)