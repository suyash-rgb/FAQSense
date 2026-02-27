import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_ROOT: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    DATABASE_URL_RAW: str = os.getenv("DATABASE_URL", "")
    
    @property
    def DATABASE_URL(self) -> str:
        # 1. Fallback to local MySQL if no env var is set or if it's the mock Render URL
        local_default = "mysql+pymysql://root:root@localhost/faqsense_db"
        
        if not self.DATABASE_URL_RAW or "render_host" in self.DATABASE_URL_RAW:
            return local_default

        # 2. Render provides postgres:// urls, but SQLAlchemy 1.4+ requires postgresql://
        if self.DATABASE_URL_RAW.startswith("postgres://"):
            return self.DATABASE_URL_RAW.replace("postgres://", "postgresql://", 1)
        
        return self.DATABASE_URL_RAW

    CLERK_WEBHOOK_SECRET: str = os.getenv("CLERK_WEBHOOK_SECRET", "")
    FUZZY_MATCH_THRESHOLD: float = float(os.getenv("FUZZY_MATCH_THRESHOLD", "80.0"))
    SEMANTIC_MATCH_THRESHOLD: float = float(os.getenv("SEMANTIC_MATCH_THRESHOLD", "0.50"))
    MIN_KEYWORD_OVERLAP: int = int(os.getenv("MIN_KEYWORD_OVERLAP", "1"))
    AMBIGUITY_THRESHOLD: float = float(os.getenv("AMBIGUITY_THRESHOLD", "0.03"))
    CONFIDENCE_THRESHOLD: float = float(os.getenv("CONFIDENCE_THRESHOLD", "0.75"))
    
    @property
    def MODEL_PATH(self) -> str:
        return os.path.join(self.PROJECT_ROOT, "models", "all-MiniLM-L6-v2")

settings = Settings()
