from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Header
from fastapi_sqlalchemy import db
from app.schemas.chatbot import ChatbotCreate, ChatbotResponse
from app.schemas.faq import FAQAskRequest, FAQAskResponse
from app.schemas.enquiry import EnquiryCreate, EnquiryUpdate, EnquiryResponse
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
    
    answer = chatbot_service.get_answer_from_chatbot(chatbot, request.question, db.session)
    
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
        # Instead of 404, we return the fallback message
        fallback_msg = "I did not understand that! Please try to rephrase your question or register your query with us."
        
        # Log fallback to conversation
        if request.conversation_id:
            from app.services import conversation_service
            conversation_service.log_message(
                db.session, 
                request.conversation_id, 
                sender="bot", 
                content=fallback_msg
            )
            
        return {"answer": fallback_msg}
    
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

@router.post("/{chatbot_id}/enquiries", response_model=EnquiryResponse)
async def register_enquiry(
    chatbot_id: int,
    enquiry_in: EnquiryCreate
):
    # Public endpoint for visitors to register their query
    chatbot = chatbot_service.get_chatbot(db.session, chatbot_id)
    if not chatbot:
        raise HTTPException(status_code=404, detail="Chatbot not found")
    
    try:
        return chatbot_service.create_enquiry(db.session, chatbot_id, enquiry_in)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{chatbot_id}/enquiries", response_model=List[EnquiryResponse])
async def list_bot_enquiries(
    chatbot_id: int,
    user_id: str = Depends(get_current_user_id)
):
    # Verify ownership
    chatbot = chatbot_service.get_chatbot(db.session, chatbot_id)
    if not chatbot or chatbot.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access these enquiries")
    
    return chatbot_service.get_enquiries(db.session, chatbot_id)

@router.patch("/{chatbot_id}/enquiries/{enquiry_id}", response_model=EnquiryResponse)
async def update_bot_enquiry(
    chatbot_id: int,
    enquiry_id: int,
    enquiry_update: EnquiryUpdate,
    user_id: str = Depends(get_current_user_id)
):
    # Verify ownership
    chatbot = chatbot_service.get_chatbot(db.session, chatbot_id)
    if not chatbot or chatbot.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to modify this enquiry")
    
    # Verify enquiry belongs to bot
    enquiry = chatbot_service.get_enquiry(db.session, enquiry_id)
    if not enquiry or enquiry.chatbot_id != chatbot_id:
        raise HTTPException(status_code=404, detail="Enquiry not found for this chatbot")
    
    updated = chatbot_service.update_enquiry(db.session, enquiry_id, enquiry_update)
    return updated

@router.get("/{chatbot_id}/top-faqs", response_model=List[str])
async def get_bot_top_faqs(
    chatbot_id: int,
    limit: int = 5
):
    # Public endpoint for frontend suggestions
    chatbot = chatbot_service.get_chatbot(db.session, chatbot_id)
    if not chatbot:
        raise HTTPException(status_code=404, detail="Chatbot not found")
    
    return chatbot_service.get_top_faqs(db.session, chatbot_id, limit)