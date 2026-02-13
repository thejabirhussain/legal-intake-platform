from openai import AsyncOpenAI
from app.core.config import settings
from typing import Dict, Any
import json

class LLMService:
    def __init__(self):
        # Initialize OpenAI Client
        self.openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        
        # Initialize Ollama Client (using OpenAI compatible endpoint)
        self.ollama_client = AsyncOpenAI(
            base_url=settings.OLLAMA_BASE_URL,
            api_key="ollama" # required but unused
        )

    async def generate_response(self, system_prompt: str, user_input: str, use_local: bool = False) -> str:
        client = self.ollama_client if use_local else self.openai_client
        model = settings.OLLAMA_MODEL if use_local else "gpt-4-turbo-preview"
        
        try:
            response = await client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.7,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"LLM Error ({'Ollama' if use_local else 'OpenAI'}): {e}")
            # Fallback to the other if one fails? For now just return error
            return "I apologize, but I am currently experiencing technical difficulties. Please try again later."

    async def extract_structured_data(self, text: str, schema: Dict[str, Any], use_local: bool = False) -> Dict[str, Any]:
        client = self.ollama_client if use_local else self.openai_client
        model = settings.OLLAMA_MODEL if use_local else "gpt-3.5-turbo-0125"
        
        # Adjust prompt for local models that might not support json mode well
        system_prompt = f"""
        Extract the following information from the text into a JSON object matching this schema:
        {json.dumps(schema)}
        
        Return ONLY the JSON object. Do not include markdown formatting or explanations.
        """
        try:
            kwargs = {}
            if "gpt" in model:
                kwargs["response_format"] = {"type": "json_object"}
                
            response = await client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": text}
                ],
                temperature=0,
                **kwargs
            )
            
            content = response.choices[0].message.content
            # Cleanup for local models that might produce markdown
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
                
            return json.loads(content)
        except Exception as e:
            print(f"Extraction Error ({'Ollama' if use_local else 'OpenAI'}): {e}")
            return {}

llm_service = LLMService()
