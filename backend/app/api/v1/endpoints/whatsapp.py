from fastapi import APIRouter, Request, HTTPException, Depends, BackgroundTasks
from app.core.config import settings
from app.schemas.whatsapp import WhatsAppWebhookPayload
from app.services.whatsapp_service import whatsapp_service

router = APIRouter()

@router.get("/webhook")
async def verify_webhook(request: Request):
    """
    Webhook verification for WhatsApp Cloud API.
    """
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode and token:
        if mode == "subscribe" and token == settings.WHATSAPP_VERIFY_TOKEN:
            return int(challenge)
        else:
            raise HTTPException(status_code=403, detail="Verification failed")
    return {"status": "ok"}

from app.agents.intake_agent import intake_agent
from app.core.database import AsyncSessionLocal

async def process_message_background(message: object):
    """
    Background task to process the message so the webhook returns 200 OK immediately.
    """
    try:
        if message.text:
            content = message.text.body
            msg_type = "text"
        elif message.image:
             content = message.image.id # In real app, download media
             msg_type = "image"
        elif message.audio:
             content = message.audio.id
             msg_type = "audio"
        else:
            return

        async with AsyncSessionLocal() as db:
            await intake_agent.process_message(db, message.from_, content, msg_type)
    except Exception as e:
        print(f"Error processing message: {e}")

@router.post("/webhook")
async def handle_webhook(payload: WhatsAppWebhookPayload, background_tasks: BackgroundTasks):
    """
    Handle incoming messages from WhatsApp.
    """
    # Simply acknowledge receipt to avoid timeouts
    # Processing happens in background
    for entry in payload.entry:
        for change in entry.changes:
            if change.value.messages:
                for message in change.value.messages:
                    background_tasks.add_task(process_message_background, message)
                    print(f"Queued message from {message.from_}")
                    
    return {"status": "received"}
