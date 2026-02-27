from app.entities.platform import Base
from app.core.config import settings
from sqlalchemy import create_engine

def init_db():
    print(f"Connecting to: {settings.DATABASE_URL}")
    engine = create_engine(settings.DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    print("All tables created successfully!")

if __name__ == "__main__":
    init_db()
