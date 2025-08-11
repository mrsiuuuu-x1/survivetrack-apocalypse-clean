import logging
import sys
import time
from pathlib import Path
from typing import Optional

def setup_logging(log_level: str = "INFO") -> logging.Logger:
    """Setup logging configuration for SurviveTrack."""
    logs_dir = Path(__file__).parent.parent.parent / "logs"
    logs_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(logs_dir / "survivetrack.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logger = logging.getLogger("SurviveTrack")
    logger.info("🔧 Logging system initialized")
    return logger

def format_time_military(timestamp: Optional[float] = None) -> str:
    """Format time in military style."""
    if timestamp is None:
        timestamp = time.time()
    return time.strftime("%H%M hrs", time.localtime(timestamp))

def create_status_message(status: str, message: str, icon: str = "📡") -> str:
    """Create a formatted status message."""
    timestamp = format_time_military()
    status_upper = status.upper()
    return f"{icon} *[{timestamp}] {status_upper}:* {message}"