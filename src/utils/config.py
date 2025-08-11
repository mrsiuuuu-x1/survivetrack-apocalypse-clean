import os
import logging
from pathlib import Path
from typing import Optional

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

class Config:
    def __init__(self):
        self.ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
        self.SERVER_PORT: int = int(os.getenv("SERVER_PORT", "7860"))
        self.SHARE_GRADIO: bool = os.getenv("SHARE_GRADIO", "true").lower() == "true"
        self.DEBUG_MODE: bool = os.getenv("DEBUG", "false").lower() == "true"
        self.LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
        self.DEFAULT_MAP_CENTER: tuple = (24.8607, 67.0011)
        self.DEFAULT_ZOOM: int = int(os.getenv("DEFAULT_ZOOM", "11"))
        self.AI_MODEL: str = os.getenv("AI_MODEL", "claude-3-haiku-20240307")
        self.AI_MAX_TOKENS: int = int(os.getenv("AI_MAX_TOKENS", "250"))
        self.AI_TEMPERATURE: float = float(os.getenv("AI_TEMPERATURE", "0.7"))
        
        self.BASE_DIR = Path(__file__).parent.parent.parent
        self.DATA_DIR = self.BASE_DIR / "data"
        self.LOGS_DIR = self.BASE_DIR / "logs"
        
        self.DATA_DIR.mkdir(exist_ok=True)
        self.LOGS_DIR.mkdir(exist_ok=True)
    
    def validate(self) -> bool:
        logger = logging.getLogger(__name__)
        if self.SERVER_PORT < 1 or self.SERVER_PORT > 65535:
            logger.error(f"Invalid server port: {self.SERVER_PORT}")
            return False
        if not self.ANTHROPIC_API_KEY:
            logger.warning("No Anthropic API key found. AI features will be disabled.")
        logger.info("Configuration validation passed")
        return True
    
    def is_ai_enabled(self) -> bool:
        return bool(self.ANTHROPIC_API_KEY)