import httpx
from app.core.config import settings

class WhatsAppService:
    def __init__(self):
        self.api_url = f"https://graph.facebook.com/v17.0/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"
        self.headers = {
            "Authorization": f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}",
            "Content-Type": "application/json",
        }

    async def send_text_message(self, to_phone: str, message_text: str):
        payload = {
            "messaging_product": "whatsapp",
            "to": to_phone,
            "type": "text",
            "text": {"body": message_text},
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(self.api_url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()

    async def send_template_message(self, to_phone: str, template_name: str, language_code: str = "en_US"):
        payload = {
            "messaging_product": "whatsapp",
            "to": to_phone,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {"code": language_code}
            }
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(self.api_url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()

whatsapp_service = WhatsAppService()
