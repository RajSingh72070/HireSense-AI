class CandidateRanking:

    @staticmethod
    def calculate_score(job_skills, resume_skills):

        if len(job_skills) == 0:
            return 0

        matched = 0

        for skill in job_skills:

            if skill.lower() in resume_skills:

                matched += 1

        score = (matched / len(job_skills)) * 100

        return round(score, 2)