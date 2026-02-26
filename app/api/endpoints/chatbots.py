from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Header
from fastapi_sqlalchemy import db
from app.schemas.chatbot import ChatbotCreate, ChatbotResponse
from app.schemas.faq import FAQAskRequest, FAQAskResponse
from app.schemas.enquiry import EnquiryCreate, EnquiryUpdate, EnquiryResponse
from app.services import chatbot_service, analytics_service
from app.schemas.analytics import ChatbotStatsResponse
from typing import List

router = APIRouter()

from app.api.deps import get_current_user_id

@router.post("/", response_model=ChatbotResponse, status_code=201)
async def create_new_chatbot(
    chatbot_in: ChatbotCreate,
    user_id: str = Depends(get_current_user_id)
):
    try:
        return chatbot_service.create_chatbot(db.session, chatbot_in, user_id)
    except Exception as e:
        print(f"ERROR: Chatbot creation failed for user_id={user_id}: {str(e)}")
        import traceback
        traceback.print_exc()
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
        return {
            "message": f"Successfully mapped {count} records to chatbot {chatbot_id}",
            "count": count
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{chatbot_id}/data")
async def get_bot_data(
    chatbot_id: int,
    user_id: str = Depends(get_current_user_id)
):
    # Verify ownership
    chatbot = chatbot_service.get_chatbot(db.session, chatbot_id)
    if not chatbot or chatbot.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this chatbot")
    
    return chatbot_service.get_chatbot_data(chatbot_id)

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
        # Resolve the session string to an internal DB ID
        conv = conversation_service.get_session_conversation(db.session, chatbot_id, request.conversation_id)
        internal_id = conv.id

        # Log visitor message
        conversation_service.log_message(
            db.session, 
            internal_id, 
            sender="visitor", 
            content=request.question
        )
        # Log bot response
        if answer:
            conversation_service.log_message(
                db.session, 
                internal_id, 
                sender="bot", 
                content=answer
            )
        else:
            conversation_service.log_message(
                db.session, 
                internal_id, 
                sender="bot", 
                content="[No answer found in knowledge base]"
            )

    if not answer:
        # Instead of 404, we return the fallback message
        fallback_msg = "I did not understand that! Please try to rephrase your question or register your query with us."
        
        # Log fallback to conversation
        if request.conversation_id:
            # We already have internal_id if it went through the above block, 
            # but let's be safe or just define it better.
            conv = conversation_service.get_session_conversation(db.session, chatbot_id, request.conversation_id)
            conversation_service.log_message(
                db.session, 
                conv.id, 
                sender="bot", 
                content=fallback_msg
            )
            
        return {"answer": fallback_msg}
    
    return {"answer": answer}

@router.post("/{chatbot_id}/click")
async def register_chatbot_click(
    chatbot_id: int
):
    # Public endpoint to track when someone clicks the toggle button
    success = analytics_service.increment_chatbot_click(db.session, chatbot_id)
    if not success:
        raise HTTPException(status_code=404, detail="Chatbot not found")
    return {"status": "success", "message": "Click recorded"}

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

@router.get("/{chatbot_id}/stats", response_model=ChatbotStatsResponse)
async def get_chatbot_analytics(
    chatbot_id: int,
    user_id: str = Depends(get_current_user_id)
):
    # Verify ownership
    chatbot = chatbot_service.get_chatbot(db.session, chatbot_id)
    if not chatbot or chatbot.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access these stats")
    
    return chatbot_service.get_chatbot_stats(db.session, chatbot_id)


