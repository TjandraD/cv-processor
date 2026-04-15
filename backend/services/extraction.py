import re

SKILL_LIST = [
    # English - Programming Languages
    "python", "javascript", "typescript", "java", "c++", "c#", "go", "golang",
    "ruby", "php", "swift", "kotlin", "scala", "r", "rust", "perl", "dart",
    "matlab", "sas", "bash", "shell scripting", "powershell",

    # English - Web Development
    "html", "css", "react", "angular", "vue", "vue.js", "node.js", "django",
    "flask", "fastapi", "spring boot", "express", "next.js", "nuxt.js",
    "rest api", "graphql", "webpack", "sass", "tailwind css", "bootstrap",

    # English - Databases
    "sql", "mysql", "postgresql", "mongodb", "redis", "sqlite", "oracle",
    "mssql", "sql server", "nosql", "elasticsearch", "cassandra", "dynamodb",

    # English - DevOps & Cloud
    "docker", "kubernetes", "aws", "gcp", "azure", "terraform", "jenkins",
    "gitlab ci", "github actions", "ansible", "linux", "nginx", "apache",

    # English - Data & ML
    "machine learning", "deep learning", "tensorflow", "pytorch", "scikit-learn",
    "data analysis", "data visualization", "data engineering", "etl",
    "statistics", "pandas", "numpy", "tableau", "power bi", "excel",
    "natural language processing", "computer vision", "mlops",

    # English - General
    "git", "agile", "scrum", "kanban", "ci/cd", "devops", "microservices",
    "api development", "unit testing", "integration testing", "tdd",
    "debugging", "code review", "system design", "architecture",
    "problem solving", "communication skills", "team leadership",
    "project management", "technical documentation",

    # English - Security & Networking
    "cybersecurity", "penetration testing", "network security", "firewall",
    "encryption", "authentication", "authorization", "oauth", "jwt",
    "networking", "tcp/ip", "dns", "http", "https",

    # English - Mobile
    "android", "ios", "flutter", "react native", "mobile development",

    # English - Other
    "blockchain", "solidity", "sap", "salesforce", "jira", "confluence",

    # Indonesian equivalents
    "pembelajaran mesin", "analisis data", "visualisasi data",
    "pengembangan perangkat lunak", "basis data", "jaringan komputer",
    "keamanan siber", "kecerdasan buatan", "pemrosesan bahasa alami",
    "pengembangan web", "pengembangan seluler", "manajemen proyek",
    "pemecahan masalah", "komunikasi", "kepemimpinan",
    "pengujian perangkat lunak", "arsitektur sistem",
]


def extract_skills(text: str) -> list:
    """Extract all skills from SKILL_LIST found in text (case-insensitive substring match)."""
    if not text or not text.strip():
        return []

    text_lower = text.lower()
    found_skills = []

    for skill in SKILL_LIST:
        skill_lower = skill.lower()
        # Use word boundaries for single-letter or very short skills to avoid false positives
        if len(skill_lower) <= 2:
            pattern = r'\b' + re.escape(skill_lower) + r'\b'
            if re.search(pattern, text_lower):
                found_skills.append(skill_lower)
        else:
            if skill_lower in text_lower:
                found_skills.append(skill_lower)

    return found_skills
