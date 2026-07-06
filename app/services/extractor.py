import re


class ResumeExtractor:

    SKILLS = [
        "python",
        "java",
        "c",
        "c++",
        "sql",
        "html",
        "css",
        "javascript",
        "fastapi",
        "flask",
        "django",
        "machine learning",
        "deep learning",
        "tensorflow",
        "pytorch",
        "opencv",
        "pandas",
        "numpy",
        "docker",
        "aws",
        "git",
        "github",
    ]

    @staticmethod
    def extract_name(text: str) -> str:
        """
        Attempts to identify the candidate's name from
        the beginning of the resume.
        """

        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        for line in lines[:10]:

            if len(line) > 60:
                continue

            if any(char.isdigit() for char in line):
                continue

            lower = line.lower()

            if "resume" in lower:
                continue

            if "curriculum" in lower:
                continue

            if "email" in lower:
                continue

            if "phone" in lower:
                continue

            if "@" in line:
                continue

            words = line.split()

            if 2 <= len(words) <= 4:
                return line.title()

        return "Unknown"

    @staticmethod
    def extract_email(text: str) -> str:

        match = re.search(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            text,
        )

        return match.group() if match else ""

    @staticmethod
    def extract_phone(text: str) -> str:

        match = re.search(
            r"\+?\d[\d\s\-]{8,15}",
            text,
        )

        return match.group().strip() if match else ""

    @staticmethod
    def extract_skills(text: str):

        text = text.lower()

        skills = []

        for skill in ResumeExtractor.SKILLS:

            if skill in text:
                skills.append(skill)

        return sorted(set(skills))