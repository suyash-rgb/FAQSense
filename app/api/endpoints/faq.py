from fastapi import APIRouter, UploadFile, File, HTTPException
from app.schemas.faq import FAQAskRequest, FAQAskResponse
from app.services import faq_service

router = APIRouter()

@router.post("/upload", status_code=201)
async def upload_faq_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")
    
    content = await file.read()
    try:
        count = faq_service.save_faq_csv(content.decode("utf-8"))
        return {"message": f"Successfully saved {count} records"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/ask", response_model=FAQAskResponse)
async def ask_faq(request: FAQAskRequest):
    answer = faq_service.get_answer_from_csv(request.question)
    if not answer:
        raise HTTPException(status_code=404, detail="Answer not found for the given question")
    return {"answer": answer}
