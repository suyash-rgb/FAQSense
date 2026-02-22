import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "mysql+pymysql://root:root@localhost/faqsense_db")
    CLERK_WEBHOOK_SECRET: str = os.getenv("CLERK_WEBHOOK_SECRET", "")
    FUZZY_MATCH_THRESHOLD: float = float(os.getenv("FUZZY_MATCH_THRESHOLD", "80.0"))
    SEMANTIC_MATCH_THRESHOLD: float = float(os.getenv("SEMANTIC_MATCH_THRESHOLD", "0.30"))

settings = Settings()
