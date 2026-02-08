from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # API Keys
    ANTHROPIC_API_KEY: str
    OPENAI_API_KEY: str
    GEMINI_API_KEY: Optional[str] = None
    GROQ_API_KEY: Optional[str] = None
    
    # App Settings
    APP_NAME: str = "GENESIS AI"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # CORS
    ALLOWED_ORIGINS: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    # File Storage
    PROJECTS_DIR: str = "./sandbox/projects"
    
    class Config:
        env_file = ".env"


settings = Settings()
