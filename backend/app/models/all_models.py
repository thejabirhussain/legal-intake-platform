import enum
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime, Enum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class UserRole(str, enum.Enum):
    ADMIN = "ADMIN"
    SENIOR_LAWYER = "SENIOR_LAWYER"
    JUNIOR_LAWYER = "JUNIOR_LAWYER"

class CaseStatus(str, enum.Enum):
    INTAKE_IN_PROGRESS = "INTAKE_IN_PROGRESS"
    PENDING_REVIEW = "PENDING_REVIEW"
    NEEDS_MORE_INFO = "NEEDS_MORE_INFO"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class MessageType(str, enum.Enum):
    TEXT = "TEXT"
    IMAGE = "IMAGE"
    AUDIO = "AUDIO"
    DOCUMENT = "DOCUMENT"

class MessageSender(str, enum.Enum):
    USER = "USER"
    AGENT = "AGENT"
    SYSTEM = "SYSTEM"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.JUNIOR_LAWYER)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)
    metadata_info = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    cases = relationship("Case", back_populates="client")

class Case(Base):
    __tablename__ = "cases"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    title = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    status = Column(Enum(CaseStatus), default=CaseStatus.INTAKE_IN_PROGRESS)
    
    # Structured data extracted by AI
    urgency = Column(String, nullable=True)
    case_type = Column(String, nullable=True)
    extracted_data = Column(JSON, default={})
    
    summary = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    client = relationship("Client", back_populates="cases")
    conversations = relationship("Conversation", back_populates="case")

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.id"))
    state = Column(String, default="START") # For State Machine
    context_data = Column(JSON, default={}) # Store temporary state data
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    case = relationship("Case", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation")

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    content = Column(Text, nullable=True)
    message_type = Column(Enum(MessageType), default=MessageType.TEXT)
    sender = Column(Enum(MessageSender), default=MessageSender.USER)
    
    media_url = Column(String, nullable=True) # S3 URL
    meta_data = Column(JSON, default={})
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    conversation = relationship("Conversation", back_populates="messages")
