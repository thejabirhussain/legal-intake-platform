from typing import List, Optional
from pydantic import BaseModel

class WhatsAppText(BaseModel):
    body: str

class WhatsAppMedia(BaseModel):
    id: str
    mime_type: str
    sha256: Optional[str] = None

class WhatsAppMessage(BaseModel):
    from_: str  # Mapped from 'from'
    id: str
    timestamp: str
    type: str
    text: Optional[WhatsAppText] = None
    image: Optional[WhatsAppMedia] = None
    audio: Optional[WhatsAppMedia] = None
    document: Optional[WhatsAppMedia] = None

    class Config:
        fields = {'from_': 'from'}

class WhatsAppContact(BaseModel):
    wa_id: str
    profile: dict

class WhatsAppChangeValue(BaseModel):
    messaging_product: str
    metadata: dict
    contacts: Optional[List[WhatsAppContact]] = None
    messages: Optional[List[WhatsAppMessage]] = None

class WhatsAppChange(BaseModel):
    value: WhatsAppChangeValue
    field: str

class WhatsAppEntry(BaseModel):
    id: str
    changes: List[WhatsAppChange]

class WhatsAppWebhookPayload(BaseModel):
    object: str
    entry: List[WhatsAppEntry]
