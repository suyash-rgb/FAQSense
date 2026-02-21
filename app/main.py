from fastapi import FastAPI
from app.api.endpoints import faq

app = FastAPI(title="FAQSense Backend")

app.include_router(faq.router, prefix="/faq", tags=["FAQ"])

@app.get("/")
async def root():
    return {"message": "Welcome to FAQSense Backend Servers"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
