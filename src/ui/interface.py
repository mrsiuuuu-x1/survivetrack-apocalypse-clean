"""
SurviveTrack User Interface
Creates the main Gradio interface with post-apocalyptic styling.
UPDATED: Now includes Request Aid and Locate Aid functionality!
"""

import logging
import time
import math
import random
from typing import List, Dict, Any

# Import your existing modules
from .styling import get_custom_css
from src.mapping.map_generator import MapGenerator
from src.mapping.zone_manager import ZoneManager
from src.ai_assistant.aria_ai import ARIAIntelligence
from src.utils.config import Config

# NEW: SOS Map Generation Functions
def generate_sos_map(lat: float, lon: float, location_name: str) -> str:
    """Generate SOS map for user's location"""
    try:
        import folium
        
        m = folium.Map(location=[lat, lon], zoom_start=15, tiles="CartoDB dark_matter")
        
        # Main SOS beacon with your original styling
        folium.Marker(
            [lat, lon],
            icon=folium.DivIcon(html=f"""
            <div style="
                background: radial-gradient(circle, #ff0000 0%, #cc0000 50%, #990000 100%);
                color: white;
                padding: 12px 16px;
                font-weight: bold;
                font-size: 12px;
                border-radius: 50%;
                text-align: center;
                animation: sos-pulse 1.5s infinite;
                box-shadow: 0 0 30px #ff0000, 0 0 60px rgba(255,0,0,0.6);
                border: 3px solid rgba(255,255,255,0.4);
                z-index: 1000;
            ">
            🆘 SOS<br><span style='font-size:10px;'>{location_name}</span>
            </div>
            <style>
            @keyframes sos-pulse {{
                0%, 100% {{ transform: scale(1); opacity: 1; }}
                50% {{ transform: scale(1.2); opacity: 0.8; }}
            }}
            </style>
            """),
            popup=f"<b>🚨 SOS SIGNAL</b><br><b>{location_name}</b><br>Time: {time.strftime('%H:%M:%S')}<br>Priority: CRITICAL"
        ).add_to(m)
        
        # Emergency radius
        folium.Circle(
            location=[lat, lon],
            radius=1000,
            color="#FF0000",
            fill=True,
            fill_opacity=0.1,
            weight=2
        ).add_to(m)
        
        # Add zombies around the perimeter
        zombie_count = 12
        for i in range(zombie_count):
            angle = (i * 360 / zombie_count) + random.uniform(-15, 15)
            angle_rad = math.radians(angle)
            
            zombie_lat = lat + (1000 / 111000) * math.cos(angle_rad)
            zombie_lon = lon + (1000 / (111000 * math.cos(math.radians(lat)))) * math.sin(angle_rad)
            
            folium.Marker(
                [zombie_lat, zombie_lon],
                icon=folium.DivIcon(html='<div style="font-size: 18px; text-shadow: 2px 2px 4px black; color: #FF0000;">🧟</div>'),
                popup=f"Zombie threat - {1000}m from SOS signal"
            ).add_to(m)
        
        return m._repr_html_()
        
    except ImportError:
        return get_fallback_map_html("SOS Map not available - install folium")
    except Exception as e:
        logging.error(f"Failed to generate SOS map: {e}")
        return get_fallback_map_html("SOS map generation failed")

def generate_aid_map(sos_zones: List[Dict]) -> str:
    """Generate map showing all SOS zones"""
    try:
        import folium
        
        m = folium.Map(location=[24.8607, 67.0011], zoom_start=11, tiles="CartoDB dark_matter")
        
        for zone in sos_zones:
            lat, lon = zone['coords']
            priority = zone['priority']
            survivors = zone['survivors']
            
            # Color based on priority
            color_map = {"CRITICAL": "#FF0000", "HIGH": "#FF6600", "MEDIUM": "#FFAA00"}
            color = color_map.get(priority, "#FF0000")
            
            # SOS marker
            folium.Marker(
                [lat, lon],
                icon=folium.DivIcon(html=f"""
                <div style="
                    background: radial-gradient(circle, {color} 0%, {color}80 50%, {color}60 100%);
                    color: white;
                    padding: 8px 12px;
                    font-weight: bold;
                    font-size: 10px;
                    border-radius: 50%;
                    text-align: center;
                    animation: aid-pulse 2s infinite;
                    box-shadow: 0 0 20px {color};
                    border: 2px solid rgba(255,255,255,0.3);
                ">
                🆘<br><span style='font-size:8px;'>{priority}</span>
                </div>
                <style>
                @keyframes aid-pulse {{
                    0%, 100% {{ transform: scale(1); opacity: 1; }}
                    50% {{ transform: scale(1.1); opacity: 0.8; }}
                }}
                </style>
                """),
                popup=f"<b>🚨 {zone['name']}</b><br>Priority: {priority}<br>Survivors: {survivors}<br>Time: {zone['time']}"
            ).add_to(m)
            
            # Priority radius
            radius_map = {"CRITICAL": 800, "HIGH": 600, "MEDIUM": 400}
            radius = radius_map.get(priority, 500)
            
            folium.Circle(
                location=[lat, lon],
                radius=radius,
                color=color,
                fill=True,
                fill_opacity=0.2,
                weight=2
            ).add_to(m)
            
            # Add zombies for high priority areas
            if priority in ["HIGH", "CRITICAL"]:
                zombie_count = 8 if priority == "CRITICAL" else 5
                
                for i in range(zombie_count):
                    angle = (i * 360 / zombie_count) + random.uniform(-30, 30)
                    distance = random.uniform(0.001, 0.003)
                    
                    zombie_lat = lat + distance * math.cos(math.radians(angle))
                    zombie_lon = lon + distance * math.sin(math.radians(angle))
                    
                    folium.Marker(
                        [zombie_lat, zombie_lon],
                        icon=folium.DivIcon(html=f'<div style="font-size: 16px; text-shadow: 1px 1px 2px black; color: {color};">🧟</div>'),
                        popup=f"Zombie near {zone['name']} ({priority} priority)"
                    ).add_to(m)
        
        return m._repr_html_()
        
    except ImportError:
        return get_fallback_map_html("Aid map not available - install folium")
    except Exception as e:
        logging.error(f"Failed to generate aid map: {e}")
        return get_fallback_map_html("Aid map generation failed")

def get_fallback_map_html(message: str) -> str:
    """Fallback HTML when map generation fails"""
    return f"""
    <div style="
        width: 100%;
        height: 400px;
        background: linear-gradient(135deg, #2c1810 0%, #1a0f08 100%);
        border: 2px solid #8B4513;
        border-radius: 8px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        color: #d4af37;
        font-family: 'Share Tech Mono', monospace;
        text-align: center;
    ">
        <div style="font-size: 48px; margin-bottom: 20px;">🗺️</div>
        <div style="font-size: 18px; font-weight: bold; margin-bottom: 10px;">
            📡 SURVIVETRACK MAP SYSTEM
        </div>
        <div style="font-size: 14px; color: #cd853f; margin-bottom: 20px;">
            {message}
        </div>
        <div style="font-size: 12px; color: #8B4513;">
            🔧 Check system dependencies
        </div>
    </div>
    """

def create_survivetrack_interface():
    """Create and configure the main Gradio interface with maps and AI."""
    try:
        import gradio as gr
    except ImportError:
        raise ImportError("Gradio not installed. Run: pip install gradio")
    
    logger = logging.getLogger(__name__)
    logger.info("🎮 Creating SurviveTrack Interface with Full Features")
    
    # Initialize systems
    config = Config()
    zone_manager = ZoneManager()
    map_generator = MapGenerator(config)
    aria_ai = ARIAIntelligence(config)
    
    # Get custom CSS
    custom_css = get_custom_css()
    
    with gr.Blocks(
        css=custom_css,
        title="SurviveTrack - The Last of Us: Karachi",
        theme=gr.themes.Base()
    ) as demo:
        
        gr.Markdown("""
        # ☣ SurviveTrack – Post-Apocalyptic Karachi Intelligence System
        ### 🏚 Twenty years after the outbreak. The city remembers.
        ### 🗺 Military-grade tactical mapping for the infected zones of Karachi 🧟‍♂
        ### 🤖 **ARIA AI Assistant** - Powered by Anthropic Claude
        ### 📦 **Resource Tracking System** - Supplies mapped by zone safety
        ### 🆘 **Emergency Response System** - SOS broadcasting and aid location
        """)
        
        with gr.Row():
            with gr.Column(scale=2):
                # UPDATED Status panel with emergency system
                gr.HTML(f"""
                <div style="
                    background: linear-gradient(135deg, rgba(15, 10, 5, 0.95) 0%, rgba(25, 15, 10, 0.90) 100%);
                    border: 2px solid rgba(218, 165, 32, 0.6);
                    border-radius: 8px;
                    padding: 16px;
                    margin-bottom: 16px;
                    font-family: 'Share Tech Mono', monospace;
                    color: #d4af37;
                ">
                    <div style="text-align: center; margin-bottom: 10px;">
                        <span style="font-size: 18px;">🎙️</span>
                        <strong> COMMUNICATION LINK ESTABLISHED</strong>
                    </div>
                    <div style="font-size: 12px;">
                        📡 SYSTEM STATUS: <span style="color: #90ee90;">OPERATIONAL</span><br>
                        🤖 ARIA AI: <span style="color: {'#00ff41' if aria_ai.is_online() else '#ff4444'};">{'ONLINE' if aria_ai.is_online() else 'OFFLINE'}</span><br>
                        📦 RESOURCE TRACKER: <span style="color: #00ff41;">ACTIVE</span><br>
                        🆘 EMERGENCY SYSTEM: <span style="color: #00ff41;">STANDBY</span><br>
                        🗺️ MAP SYSTEM: <span style="color: #00ff41;">OPERATIONAL</span><br>
                        🌍 SCAN RADIUS: 50km KARACHI ZONE<br>
                        ⚠️ THREAT LEVEL: <span style="color: #ff4444;">CRITICAL</span>
                    </div>
                </div>
                """)
                
                chatbot = gr.Chatbot(
                    value=[["🎯 ARIA", "🤖 SurviveTrack fully operational! All systems online including emergency response. Interactive maps, AI assistance, and SOS features ready for deployment."]],
                    height=400,
                    show_label=False
                )
                
                with gr.Row():
                    msg = gr.Textbox(
                        placeholder="🎯 [ENCRYPTED COMMS] Zone designation (A|B|C) or tactical query...",
                        scale=6,
                        container=False,
                        show_label=False
                    )
                    send_btn = gr.Button("📻 RELAY", scale=1, variant="primary")
                
                with gr.Row():
                    zone_a_btn = gr.Button("⚠ SECTOR-A", scale=1, variant="secondary")
                    zone_b_btn = gr.Button("☢ SECTOR-B", scale=1, variant="secondary")
                    zone_c_btn = gr.Button("🚂 SECTOR-C", scale=1, variant="secondary")
                    resource_btn = gr.Button("📦 RESOURCES", scale=1, variant="secondary")
                
                # NEW: Emergency Response Row
                with gr.Row():
                    request_aid_btn = gr.Button("🆘 REQUEST AID", scale=1, variant="stop")
                    locate_aid_btn = gr.Button("🔍 LOCATE AID", scale=1, variant="secondary")
            
            with gr.Column(scale=3):
                gr.Markdown("### 🗺 *[TACTICAL OVERVIEW] Infected Territory Mapping System*")
                gr.Markdown("#### 📦 Resource markers: 💧🍞🏠 (Zone A) | 💊🔦 (Zone B) | 🔫🩺 (Zone C)")
                gr.Markdown("#### 🆘 Emergency features: SOS broadcasting | Aid location | Crisis response")
                
                # Interactive map with your original system
                map_output = gr.HTML(
                    value=map_generator.generate_overview_map(show_welcome=True)
                )
        
        def respond(message, history):
            """Handle chat responses with AI and map integration"""
            if not message:
                return history, map_generator.generate_overview_map()
            
            message_lower = message.lower()
            
            # Check for zone requests - YOUR ORIGINAL ZONE SYSTEM
            for zone_key in ["Zone A", "Zone B", "Zone C"]:
                if zone_key.lower() in message_lower or zone_key.replace(" ", "").lower() in message_lower:
                    zone = zone_manager.get_zone(zone_key)
                    if zone:
                        # Get AI response for the zone
                        zone_dict = {
                            'name': zone.name,
                            'danger': zone.danger,
                            'resources': zone.resources,
                            'alert': zone.alert,
                            'description': zone.description
                        }
                        
                        ai_response = aria_ai.get_response(
                            f"User is asking about {zone_key}. Provide tactical intel and survival advice.",
                            zone_dict
                        )
                        
                        reply = f"""🎯 **{zone.name}**

📦 **Resources Available:**
{chr(10).join('   • ' + r for r in zone.resources)}

🚨 **Current Status:** {zone.alert}

🤖 **ARIA Analysis:**
{ai_response}

📡 Zooming to location..."""
                        
                        history.append((message, reply))
                        # Generate zone map with cinematic effects
                        zone_map = map_generator.generate_zone_map(zone_key, {zone_key: zone}, cinematic=True)
                        return history, zone_map
            
            # Resource scan
            if "resource" in message_lower:
                ai_analysis = aria_ai.get_response("All resource locations are now visible across Karachi. Provide tactical analysis of resource distribution.")
                
                reply = f"""📦 **RESOURCE LOCATOR SCAN COMPLETE**

🌍 **Scan Radius:** Full Karachi Zone
📍 **Zones Scanned:** 3 Active
⏰ **Scan Time:** Live

📦 **Resource Summary:**
   • Zone A (Boat Basin): HIGH density - Water, Food, Shelter
   • Zone B (Lyari): MEDIUM density - Medicine, Equipment  
   • Zone C (Railway): LOW density - Weapons, Military Supplies

🤖 **ARIA Resource Analysis:**
{ai_analysis}"""
                
                history.append((message, reply))
                return history, map_generator.generate_overview_map(show_welcome=False)
            
            # General AI response
            ai_response = aria_ai.get_response(message)
            reply = f"🤖 **ARIA Response:**\n\n{ai_response}"
            
            history.append((message, reply))
            return history, map_generator.generate_overview_map(show_welcome=False)
        
        def quick_zone_select(zone_key, history):
            """Handle quick zone selection buttons"""
            zone = zone_manager.get_zone(zone_key)
            if not zone:
                return history, map_generator.generate_overview_map()
            
            zone_dict = {
                'name': zone.name,
                'danger': zone.danger,
                'resources': zone.resources,
                'alert': zone.alert,
                'description': zone.description
            }
            
            ai_insight = aria_ai.get_response(f"Provide a quick tactical brief for {zone_key} access.", zone_dict)
            
            reply = f"""⚡ **Quick Access: {zone.name}**

📦 Resources: {', '.join(zone.resources)}
🚨 Status: {zone.alert}

🤖 **ARIA Brief:** {ai_insight}

🎯 Initiating tactical zoom..."""
            
            history.append((f"[Quick Select {zone_key}]", reply))
            zone_map = map_generator.generate_zone_map(zone_key, {zone_key: zone}, cinematic=True)
            return history, zone_map
        
        # NEW: SOS Functions
        def request_aid(history):
            """Handle SOS request - YOUR ORIGINAL SOS SYSTEM"""
            # Use specific coordinates for consistent demo
            live_lat = 24.87366765011169
            live_lon = 67.073671736837
            
            # Get AI assessment
            sos_assessment = aria_ai.get_response(f"A survivor is requesting emergency aid at coordinates {live_lat:.4f}, {live_lon:.4f}. Provide emergency response guidance and survival tips.")
            
            reply = f"""🚨 **SOS SIGNAL TRANSMITTED**

📍 **Your Location:** {live_lat:.4f}, {live_lon:.4f}
⏰ **Time:** {time.strftime('%H:%M:%S')}
📡 **Signal Strength:** EXCELLENT
🆘 **Aid Request:** ACTIVE

💬 **Message:** 'Survivor in distress. Need immediate assistance.'
🎯 **Priority:** CRITICAL

🤖 **ARIA Emergency Protocol:**
{sos_assessment}

⚠️ **Warning:** Stay hidden. Help is on the way."""
            
            history.append(("[SOS REQUEST]", reply))
            sos_map = generate_sos_map(live_lat, live_lon, "YOUR LOCATION")
            return history, sos_map
        
        def locate_aid(history):
            """Handle aid location - YOUR ORIGINAL AID SYSTEM"""
            # Generate random SOS zones across Karachi
            sos_zones = []
            for i in range(5):
                lat = 24.8607 + random.uniform(-0.1, 0.1)
                lon = 67.0011 + random.uniform(-0.1, 0.1)
                sos_zones.append({
                    'coords': [lat, lon],
                    'name': f"Distress Signal #{i+1}",
                    'time': f"{random.randint(0, 23):02d}:{random.randint(0, 59):02d}",
                    'priority': random.choice(['CRITICAL', 'HIGH', 'MEDIUM']),
                    'survivors': random.randint(1, 8)
                })
            
            # Get AI recommendation
            aid_analysis = aria_ai.get_response(f"Multiple SOS signals detected across Karachi. {len(sos_zones)} active distress calls with varying priority levels. Provide tactical recommendation for aid response prioritization.")
            
            reply = f"""🔍 **AID LOCATION SCAN COMPLETE**

📡 **Active SOS Signals:** {len(sos_zones)}
🌍 **Scan Radius:** 20km
⏰ **Scan Time:** {time.strftime('%H:%M:%S')}

🚨 **Priority Signals:**"""
            
            for i, zone in enumerate(sos_zones[:3]):
                reply += f"\n   • {zone['name']} - {zone['priority']} - {zone['survivors']} survivors"
            
            reply += f"\n\n🤖 **ARIA Tactical Recommendation:**\n{aid_analysis}"
            
            history.append(("[AID LOCATOR]", reply))
            aid_map = generate_aid_map(sos_zones)
            return history, aid_map
        
        # Event handlers
        msg.submit(respond, [msg, chatbot], [chatbot, map_output])
        send_btn.click(respond, [msg, chatbot], [chatbot, map_output])
        
        zone_a_btn.click(lambda h: quick_zone_select("Zone A", h), [chatbot], [chatbot, map_output])
        zone_b_btn.click(lambda h: quick_zone_select("Zone B", h), [chatbot], [chatbot, map_output])
        zone_c_btn.click(lambda h: quick_zone_select("Zone C", h), [chatbot], [chatbot, map_output])
        
        resource_btn.click(lambda h: respond("resources", h), [chatbot], [chatbot, map_output])
        
        # NEW: SOS button handlers
        request_aid_btn.click(request_aid, [chatbot], [chatbot, map_output])
        locate_aid_btn.click(locate_aid, [chatbot], [chatbot, map_output])
        
        # Clear message box
        msg.submit(lambda: "", outputs=[msg])
        send_btn.click(lambda: "", outputs=[msg])
    
    return demo