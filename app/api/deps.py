from fastapi import Header, HTTPException, Depends
from fastapi_sqlalchemy import db
from app.models.platform import User

async def get_current_user_id(x_user_id: str = Header(...)):
    # In a real app, this would verify a JWT token
    query = db.session.query(User).filter(User.clerk_id == x_user_id)
    user = query.first()
    if not user:
        print(f"Lazy-onboarding user: {x_user_id}")
        user = User(
            clerk_id=x_user_id, 
            email=f"{x_user_id}@example.com", 
            full_name="User " + x_user_id[:8]
        )
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
    return x_user_id
