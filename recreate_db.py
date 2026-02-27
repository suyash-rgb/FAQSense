from app.entities.platform import Base
from app.core.config import settings
from sqlalchemy import create_engine

def recreate_db():
    print(f"Connecting to: {settings.DATABASE_URL}")
    engine = create_engine(settings.DATABASE_URL)
    
    # Drop all tables
    print("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    
    # Create all tables
    print("Recreating all tables...")
    Base.metadata.create_all(bind=engine)
    
    print("Database scheme reset successfully!")

if __name__ == "__main__":
    recreate_db()
