from typing import List, Optional, Union
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyHttpUrl, PostgresDsn, validator

class Settings(BaseSettings):
    PROJECT_NAME: str = "Smart Lawyer Assistant"
    API_V1_STR: str = "/api/v1"
    
    # SECURITY
    SECRET_KEY: str = "unsafe-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # DATABASE
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/smart_lawyer"
    
    # EXTERNAL APIS
    OPENAI_API_KEY: str
    WHATSAPP_ACCESS_TOKEN: str
    WHATSAPP_PHONE_NUMBER_ID: str
    WHATSAPP_VERIFY_TOKEN: str
    
    # OLLAMA
    OLLAMA_BASE_URL: str = "http://host.docker.internal:11434/v1"
    OLLAMA_MODEL: str = "llama3:8b"
    
    # S3 / STORAGE
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_BUCKET_NAME: str = "smart-lawyer-uploads"
    AWS_REGION: str = "us-east-1"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[Union[str, AnyHttpUrl]] = ["http://localhost:5173", "http://localhost:3000", "http://localhost:5174"]

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

settings = Settings()
