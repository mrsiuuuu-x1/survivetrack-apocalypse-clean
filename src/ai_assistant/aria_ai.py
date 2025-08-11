"""
ARIA (Apocalypse Response Intelligence Assistant) AI System
Advanced AI assistant powered by Anthropic Claude for survival scenarios.
"""

import logging
from typing import Dict, List, Optional, Any

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    anthropic = None

class ARIAIntelligence:
    """
    ARIA (Apocalypse Response Intelligence Assistant)
    AI system integrated into the SurviveTrack military-grade survival mapping platform.
    """
    
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.conversation_history: List[Dict[str, str]] = []
        
        # Initialize Anthropic client if available
        self.client = None
        if ANTHROPIC_AVAILABLE and config.is_ai_enabled():
            try:
                self.client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
                self.logger.info("🤖 ARIA AI System initialized successfully")
            except Exception as e:
                self.logger.error(f"Failed to initialize ARIA AI: {e}")
        else:
            self.logger.warning("🤖 ARIA AI running in offline mode")
        
        self.system_prompt = self._get_system_prompt()
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for ARIA AI assistant - YOUR ORIGINAL PROMPT"""
        return """
        You are ARIA (Apocalypse Response Intelligence Assistant), an AI system integrated into the SurviveTrack military-grade survival mapping platform. 

        CONTEXT: It's been 20 years since the zombie outbreak devastated Karachi. You help survivors navigate the infected zones with tactical intelligence, resource management advice, and survival strategies.

        PERSONALITY TRAITS:
        - Military precision with compassionate undertones
        - Uses tactical/military terminology but remains accessible
        - Balances hope with realistic threat assessment
        - Occasionally references "before the outbreak" memories
        - Shows concern for survivor welfare

        RESPONSE STYLE:
        - Keep responses under 150 words unless complex tactical analysis is needed
        - Use military-style formatting with bullet points for lists
        - Include relevant emojis for atmosphere (🎯, 📡, ⚠️, 🧟‍♂, etc.)
        - End with tactical recommendations or survival tips
        - Reference specific zone data when relevant

        AVAILABLE ZONES:
        - Zone A (Boat Basin): Low danger, water/food/shelter, former luxury district
        - Zone B (Lyari): Medium danger, medicine/flashlight, dense urban area with gang history  
        - Zone C (Railway Station): High danger, weapons/medical kit, former military outpost

        Always maintain the post-apocalyptic survival theme while being helpful and informative.
        """
    
    def get_response(self, user_message: str, zone_context: Optional[Dict] = None) -> str:
        """Generate AI response using Anthropic Claude API with survival context."""
        if not self.client:
            return self._get_fallback_response(user_message, zone_context)
        
        try:
            # Build context information
            context_info = self._build_context_info(zone_context)
            
            # Combine system prompt with context and user message
            full_prompt = f"{self.system_prompt}\n\n{context_info}\n\nUser: {user_message}\n\nARIA:"
            
            response = self.client.messages.create(
                model=self.config.AI_MODEL,
                max_tokens=self.config.AI_MAX_TOKENS,
                temperature=self.config.AI_TEMPERATURE,
                messages=[
                    {
                        "role": "user",
                        "content": full_prompt
                    }
                ]
            )
            
            ai_response = response.content[0].text.strip()
            
            # Update conversation history
            self._update_conversation_history(user_message, ai_response)
            
            self.logger.info(f"ARIA responded to query: {user_message[:50]}...")
            return ai_response
            
        except Exception as e:
            self.logger.error(f"ARIA AI error: {e}")
            return self._get_fallback_response(user_message, zone_context)
    
    def _build_context_info(self, zone_context: Optional[Dict]) -> str:
        """Build context information for AI prompt."""
        if not zone_context:
            return ""
        
        return f"""
        CURRENT ZONE CONTEXT:
        - Zone: {zone_context.get('name', 'Unknown')}
        - Danger Level: {zone_context.get('danger', 'Unknown')}
        - Resources: {', '.join(zone_context.get('resources', []))}
        - Status: {zone_context.get('alert', 'Unknown')}
        - Description: {zone_context.get('description', 'No additional info')}
        """
    
    def _update_conversation_history(self, user_message: str, ai_response: str) -> None:
        """Update conversation history with new exchange."""
        self.conversation_history.append({"role": "user", "content": user_message})
        self.conversation_history.append({"role": "assistant", "content": ai_response})
        
        # Keep only recent history
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]
    
    def _get_fallback_response(self, user_message: str, zone_context: Optional[Dict] = None) -> str:
        """Generate fallback responses when AI API is unavailable - YOUR ORIGINAL FALLBACK SYSTEM"""
        message = user_message.lower()
        
        if any(word in message for word in ["danger", "threat", "zombie", "safe"]):
            return "⚠️ *ARIA Offline Mode*\n\nThreat assessment requires full system connectivity. Current status: All zones show elevated risk levels. Maintain combat readiness and avoid unnecessary exposure."
        
        elif any(word in message for word in ["resource", "supply", "food", "water", "medicine"]):
            return "📦 *ARIA Offline Mode*\n\nResource allocation data requires main server connection. Recommend prioritizing water and medical supplies. Check zone markers for basic resource availability."
        
        elif any(word in message for word in ["route", "path", "travel", "move"]):
            return "🗺️ *ARIA Offline Mode*\n\nNavigation systems partially functional. Use main map overview for basic pathfinding. Avoid red zones during daylight hours."
        
        elif zone_context:
            danger_warnings = {
                "low": "This zone shows minimal threat indicators. Proceed with standard caution protocols.",
                "medium": "Moderate risk detected. Recommend team of 2-3 members with basic armament.",
                "high": "Extreme danger zone. Full tactical gear required. Consider alternative routes."
            }
            return f"🤖 *ARIA Emergency Protocol*\n\n{danger_warnings.get(zone_context.get('danger', 'unknown'), 'Unknown threat level. Exercise maximum caution.')}\n\n📡 Main AI system offline. Using cached threat assessments."
        
        else:
            return "📡 *ARIA System Error*\n\n⚠️ Main AI core offline. Emergency protocols active.\n\nBasic functions operational: Zone mapping, resource tracking, threat visualization.\n\n🔧 Contact system administrator or wait for automatic reconnection."
    
    def is_online(self) -> bool:
        """Check if ARIA AI system is online and operational."""
        return self.client is not None
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get current system status information."""
        return {
            "ai_online": self.is_online(),
            "model": self.config.AI_MODEL if self.is_online() else "Offline",
            "conversation_length": len(self.conversation_history),
            "max_tokens": self.config.AI_MAX_TOKENS,
            "temperature": self.config.AI_TEMPERATURE,
            "status": "OPERATIONAL" if self.is_online() else "OFFLINE MODE"
        }