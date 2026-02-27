from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime
import uuid

Base = declarative_base()

class Admin(Base):
    __tablename__ = "admins"
    id = Column(String(255), primary_key=True)
    email = Column(String(255), unique=True, index=True)
    full_name = Column(String(255))

class User(Base):
    __tablename__ = "users"
    clerk_id = Column(String(255), primary_key=True)
    email = Column(String(255), unique=True, index=True)
    full_name = Column(String(255))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    chatbots = relationship("Chatbot", back_populates="owner")

class Visitor(Base):
    __tablename__ = "visitors"
    id = Column(String(255), primary_key=True) # UUID or Session ID
    first_seen = Column(DateTime, default=datetime.datetime.utcnow)
    
    conversations = relationship("Conversation", back_populates="visitor")

class Chatbot(Base):
    __tablename__ = "chatbots"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(255), ForeignKey("users.clerk_id"))
    name = Column(String(255))
    csv_file_path = Column(String(255))
    click_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    owner = relationship("User", back_populates="chatbots")
    conversations = relationship("Conversation", back_populates="chatbot", cascade="all, delete-orphan")
    enquiries = relationship("Enquiry", back_populates="chatbot", cascade="all, delete-orphan")
    analytics = relationship("FAQAnalytics", back_populates="chatbot", cascade="all, delete-orphan")

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(String(255), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    chatbot_id = Column(Integer, ForeignKey("chatbots.id"))
    visitor_id = Column(String(255), ForeignKey("visitors.id"))
    started_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    chatbot = relationship("Chatbot", back_populates="conversations")
    visitor = relationship("Visitor", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation")

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(String(255), ForeignKey("conversations.id"))
    sender = Column(String(50)) # "visitor" or "bot"
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    conversation = relationship("Conversation", back_populates="messages")

class Enquiry(Base):
    __tablename__ = "enquiries"
    id = Column(Integer, primary_key=True, index=True)
    chatbot_id = Column(Integer, ForeignKey("chatbots.id"))
    query_text = Column(Text)
    visitor_name = Column(String(255))
    visitor_email = Column(String(255), nullable=True)
    visitor_phone = Column(String(50), nullable=True)
    status = Column(String(50), default="open") # "open", "resolved"
    admin_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    chatbot = relationship("Chatbot", back_populates="enquiries")

class FAQAnalytics(Base):
    __tablename__ = "faq_analytics"
    id = Column(Integer, primary_key=True, index=True)
    chatbot_id = Column(Integer, ForeignKey("chatbots.id"))
    original_question = Column(Text)
    hit_count = Column(Integer, default=0)
    last_hit_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    chatbot = relationship("Chatbot", back_populates="analytics")
