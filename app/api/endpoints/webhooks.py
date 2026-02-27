from fastapi import APIRouter, Header, Request, HTTPException
from fastapi_sqlalchemy import db
from app.entities.platform import User
from app.core.config import settings
from svix.webhooks import Webhook, WebhookVerificationError
import json

router = APIRouter()

@router.post("/clerk")
async def clerk_webhook(
    request: Request,
    svix_id: str = Header(None, alias="svix-id"),
    svix_signature: str = Header(None, alias="svix-signature"),
    svix_timestamp: str = Header(None, alias="svix-timestamp"),
):
    # Retrieve the raw body
    body = await request.body()
    payload_str = body.decode("utf-8")
    
    headers = {
        "svix-id": svix_id,
        "svix-signature": svix_signature,
        "svix-timestamp": svix_timestamp,
    }

    if not all([svix_id, svix_signature, svix_timestamp]):
        raise HTTPException(status_code=400, detail="Missing svix headers")

    if not settings.CLERK_WEBHOOK_SECRET:
        print("WARNING: CLERK_WEBHOOK_SECRET not set. Skipping verification (Insecure!)")
    else:
        try:
            wh = Webhook(settings.CLERK_WEBHOOK_SECRET)
            wh.verify(payload_str, headers)
        except WebhookVerificationError as e:
            raise HTTPException(status_code=400, detail="Invalid signature")

    payload = json.loads(payload_str)
    event_type = payload.get("type")
    data = payload.get("data")
    
    if event_type in ["user.created", "user.updated"]:
        clerk_id = data.get("id")
        email = data.get("email_addresses")[0].get("email_address") if data.get("email_addresses") else None
        first_name = data.get("first_name", "")
        last_name = data.get("last_name", "")
        full_name = f"{first_name} {last_name}".strip()
        
        # Upsert User
        user = db.session.query(User).filter(User.clerk_id == clerk_id).first()
        if not user:
            user = User(clerk_id=clerk_id, email=email, full_name=full_name)
            db.session.add(user)
        else:
            user.email = email
            user.full_name = full_name
        
        db.session.commit()
        return {"status": "success", "message": "User synced"}
    
    return {"status": "ignored"}
