#!/usr/bin/env python3
"""
SurviveTrack - Post-Apocalyptic Karachi Intelligence System
Main application entry point

Created for Cedar Codes: Apocalypse Hackathon 2025
Authors: Abdul Rafay & Laksh Mandhan
"""

import os
import sys
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def main():
    """
    Main entry point for SurviveTrack application.
    Sets up logging, validates configuration, and launches the Gradio interface.
    """
    try:
        from src.ui.interface import create_survivetrack_interface
        from src.utils.config import Config
        from src.utils.helpers import setup_logging
        
        # Setup logging
        logger = setup_logging()
        logger.info("🚀 Starting SurviveTrack - Post-Apocalyptic Intelligence System")
        
        # Validate configuration
        config = Config()
        if not config.validate():
            logger.error("❌ Configuration validation failed. Check your .env file.")
            sys.exit(1)
        
        logger.info("✅ Configuration validated successfully")
        logger.info(f"🤖 ARIA AI System: {'ONLINE' if config.ANTHROPIC_API_KEY else 'OFFLINE'}")
        
        # Create and launch the interface
        demo = create_survivetrack_interface()
        
        logger.info("🌍 Launching SurviveTrack interface...")
        logger.info(f"📡 Server will be available at: http://localhost:{config.SERVER_PORT}")
        logger.info("⚠️  WARNING: This is a simulation for hackathon purposes only")
        
        # Launch the application
        demo.launch(
            share=config.SHARE_GRADIO,
            server_port=config.SERVER_PORT,
            show_error=True,
            server_name="0.0.0.0" if config.SHARE_GRADIO else "127.0.0.1"
        )
        
    except KeyboardInterrupt:
        print("🛑 Application interrupted by user")
    except ImportError as e:
        print(f"❌ Missing dependencies. Please run: pip install -r requirements.txt")
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"💥 Application crashed: {str(e)}")
        print("Check the logs for more details.")
        raise
    finally:
        print("📻 SurviveTrack shutting down... Stay safe out there!")

if __name__ == "__main__":
    main()