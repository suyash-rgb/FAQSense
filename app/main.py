from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi_sqlalchemy import DBSessionMiddleware, db
from sqlalchemy import create_engine
from app.api.endpoints import faq, webhooks, chatbots, conversations
from app.core.config import settings
from app.entities.platform import Base

# Create tables on startup
engine = create_engine(settings.DATABASE_URL)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FAQSense Backend")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Add DB Middleware
app.add_middleware(DBSessionMiddleware, db_url=settings.DATABASE_URL)

app.include_router(faq.router, prefix="/faq", tags=["FAQ"])
app.include_router(webhooks.router, prefix="/webhooks", tags=["Webhooks"])
app.include_router(chatbots.router, prefix="/chatbots", tags=["Chatbots"])
app.include_router(conversations.router, prefix="/conversations", tags=["Conversations"])

@app.get("/")
async def root():
    return {"message": "Welcome to FAQSense Backend Servers"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
