from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Header
from fastapi_sqlalchemy import db
from app.schemas.chatbot import ChatbotCreate, ChatbotResponse
from app.schemas.faq import FAQAskRequest, FAQAskResponse
from app.services import chatbot_service
from typing import List

router = APIRouter()

# Helper to get user_id from header for dev purposes
async def get_current_user_id(x_user_id: str = Header(...)):
    # In a real app, this would verify a JWT token
    return x_user_id

@router.post("/", response_model=ChatbotResponse, status_code=201)
async def create_new_chatbot(
    chatbot_in: ChatbotCreate,
    user_id: str = Depends(get_current_user_id)
):
    try:
        return chatbot_service.create_chatbot(db.session, chatbot_in, user_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[ChatbotResponse])
async def list_chatbots(
    user_id: str = Depends(get_current_user_id)
):
    return chatbot_service.get_user_chatbots(db.session, user_id)

@router.post("/{chatbot_id}/upload")
async def upload_bot_csv(
    chatbot_id: int,
    file: UploadFile = File(...),
    user_id: str = Depends(get_current_user_id)
):
    # Verify ownership
    chatbot = chatbot_service.get_chatbot(db.session, chatbot_id)
    if not chatbot or chatbot.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this chatbot")

    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")
    
    content = await file.read()
    try:
        count = chatbot_service.save_chatbot_csv(db.session, chatbot_id, content.decode("utf-8"))
        return {"message": f"Successfully mapped {count} records to chatbot {chatbot_id}"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{chatbot_id}/ask", response_model=FAQAskResponse)
async def ask_bot(
    chatbot_id: int,
    request: FAQAskRequest
):
    # Public endpoint (no user_id check typically, as visitors use this)
    chatbot = chatbot_service.get_chatbot(db.session, chatbot_id)
    if not chatbot:
        raise HTTPException(status_code=404, detail="Chatbot not found")
    
    answer = chatbot_service.get_answer_from_chatbot(chatbot, request.question)
    
    # Log to conversation if ID provided
    if request.conversation_id:
        from app.services import conversation_service
        # Log visitor message
        conversation_service.log_message(
            db.session, 
            request.conversation_id, 
            sender="visitor", 
            content=request.question
        )
        # Log bot response
        if answer:
            conversation_service.log_message(
                db.session, 
                request.conversation_id, 
                sender="bot", 
                content=answer
            )
        else:
            conversation_service.log_message(
                db.session, 
                request.conversation_id, 
                sender="bot", 
                content="[No answer found in knowledge base]"
            )

    if not answer:
        raise HTTPException(status_code=404, detail="Answer not found in this chatbot's database")
    
    return {"answer": answer}

@router.get("/{chatbot_id}", response_model=ChatbotResponse)
async def get_chatbot(
    chatbot_id: int,
    user_id: str = Depends(get_current_user_id)
):
    chatbot = chatbot_service.get_chatbot(db.session, chatbot_id)
    if not chatbot or chatbot.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this chatbot")
    return chatbot

@router.delete("/{chatbot_id}")
async def delete_chatbot(
    chatbot_id: int,
    user_id: str = Depends(get_current_user_id)
):
    chatbot = chatbot_service.get_chatbot(db.session, chatbot_id)
    if not chatbot or chatbot.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this chatbot")
    chatbot_service.delete_chatbot(db.session, chatbot_id)
    return {"message": f"Chatbot {chatbot_id} deleted successfully"}