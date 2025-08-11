"""
Interactive Map Generation System for SurviveTrack
Creates folium maps with zones, resources, and tactical overlays.
"""

import math
import random
import time
import logging

try:
    import folium
    FOLIUM_AVAILABLE = True
except ImportError:
    FOLIUM_AVAILABLE = False
    folium = None

class MapGenerator:
    """Generates interactive maps with tactical overlays for SurviveTrack."""
    
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        if not FOLIUM_AVAILABLE:
            self.logger.error("Folium not available. Map generation will be limited.")
        else:
            self.logger.info("🗺️ Map Generator initialized successfully")
    
    def generate_overview_map(self, show_welcome: bool = False) -> str:
        """Generate overview map of all zones in Karachi - YOUR ORIGINAL MAP SYSTEM"""
        if not FOLIUM_AVAILABLE:
            return self._get_fallback_map_html("Install folium: pip install folium")
        
        try:
            # Create base map centered on Karachi
            m = folium.Map(
                location=[24.8607, 67.0011],  # Karachi coordinates
                zoom_start=11,
                tiles="CartoDB dark_matter"
            )
            
            if not show_welcome:
                self._add_zone_overview_markers(m)
            
            return m._repr_html_()
            
        except Exception as e:
            self.logger.error(f"Failed to generate overview map: {e}")
            return self._get_fallback_map_html("Map generation failed")
    
    def generate_zone_map(self, zone_key: str, zone_data: dict, cinematic: bool = True) -> str:
        """Generate detailed map for a specific zone - YOUR ORIGINAL ZONE MAPS"""
        if not FOLIUM_AVAILABLE:
            return self._get_fallback_map_html(f"Zone {zone_key} map not available")
        
        try:
            zone = zone_data.get(zone_key)
            if not zone:
                return self._get_fallback_map_html(f"Zone {zone_key} not found")
            
            # Create map centered on zone
            m = folium.Map(
                location=zone.coords,
                zoom_start=16,
                tiles="CartoDB dark_matter"
            )
            
            # Add zone-specific markers
            self._add_zone_detailed_markers(m, zone)
            self._add_resource_markers(m, zone)
            self._add_zombie_markers(m, zone)
            self._add_danger_indicators(m, zone)
            
            # Add cinematic effects
            map_html = m._repr_html_()
            if cinematic:
                map_html = self._add_cinematic_effects(map_html, zone)
            
            return map_html
            
        except Exception as e:
            self.logger.error(f"Failed to generate zone map for {zone_key}: {e}")
            return self._get_fallback_map_html(f"Zone {zone_key} map generation failed")
    
    def _add_zone_overview_markers(self, map_obj):
        """Add zone markers for overview map - YOUR ORIGINAL ZONE_DATA"""
        zones = {
            "Zone A": {
                "coords": [24.8182, 67.0256],
                "danger": "low",
                "name": "📍 Zone A – Boat Basin",
                "alert": "🟢 Clear. No zombies spotted.",
                "resources": ["💧 Water", "🍞 Food", "🏠 Shelter"]
            },
            "Zone B": {
                "coords": [24.8784, 67.0103], 
                "danger": "medium",
                "name": "📍 Zone B – Lyari",
                "alert": "🧟‍♂ Danger! Zombie activity nearby. 🚨",
                "resources": ["💊 Medicine", "🔦 Flashlight"]
            },
            "Zone C": {
                "coords": [24.9090, 67.0940],
                "danger": "high", 
                "name": "📍 Zone C – Railway Station",
                "alert": "🔴 Safe for now, but stay alert. 👀",
                "resources": ["🔫 Weapons", "🩺 Medical Kit"]
            }
        }
        
        for zone_key, zone_info in zones.items():
            color_map = {"low": "green", "medium": "orange", "high": "red"}
            marker_color = color_map.get(zone_info["danger"], "red")
            
            # Enhanced SOS Distress Beacon - The Last of Us style
            folium.Marker(
                zone_info["coords"],
                popup=f"<b>{zone_info['name']}</b><br>{zone_info['alert']}<br>Resources: {', '.join(zone_info['resources'])}",
                icon=folium.Icon(color=marker_color, icon="info-sign"),
                tooltip=zone_info["name"]
            ).add_to(map_obj)
            
            # Add circles around zones
            folium.CircleMarker(
                location=zone_info["coords"],
                radius=40,
                color=marker_color,
                fill=True,
                fill_opacity=0.3,
                weight=2
            ).add_to(map_obj)
            
            # Add resource markers inside zone circles
            self._add_overview_resource_markers(map_obj, zone_info)
            
            # Add zombie markers for high danger zones
            if zone_info["danger"] == "high":
                self._add_overview_zombie_markers(map_obj, zone_info)
    
    def _add_overview_resource_markers(self, map_obj, zone_info):
        """Add resource markers for overview - YOUR ORIGINAL RESOURCE SYSTEM"""
        coords = zone_info["coords"]
        
        if zone_info["danger"] == "low":  # Zone A - abundant resources
            positions = [
                [coords[0] + 0.0008, coords[1] - 0.0008, "💧"],
                [coords[0] - 0.0008, coords[1] + 0.0008, "🍞"],
                [coords[0] + 0.0006, coords[1] + 0.0006, "🏠"],
                [coords[0] - 0.0006, coords[1] - 0.0006, "💧"],
            ]
        elif zone_info["danger"] == "medium":  # Zone B - medical supplies
            positions = [
                [coords[0] + 0.0008, coords[1] - 0.0008, "💊"],
                [coords[0] - 0.0008, coords[1] + 0.0008, "🔦"],
            ]
        else:  # Zone C - military equipment
            positions = [
                [coords[0] + 0.0008, coords[1] - 0.0008, "🔫"],
                [coords[0] - 0.0008, coords[1] + 0.0008, "🩺"],
            ]
        
        for lat, lon, emoji in positions:
            folium.Marker(
                [lat, lon],
                icon=folium.DivIcon(html=f"""
                <div style="
                    font-size: 12px;
                    text-shadow: 1px 1px 2px black;
                    opacity: 0.8;
                ">
                {emoji}
                </div>
                """),
                popup=f"<b>📦 Resource</b><br>Zone: {zone_info['name']}<br>Type: {emoji}",
                tooltip=f"{emoji} Resource"
            ).add_to(map_obj)
    
    def _add_overview_zombie_markers(self, map_obj, zone_info):
        """Add zombie markers for high danger zones"""
        coords = zone_info["coords"]
        zombie_positions = [
            [coords[0] + 0.002, coords[1] - 0.002],
            [coords[0] - 0.002, coords[1] + 0.002],
            [coords[0] + 0.001, coords[1] + 0.001],
            [coords[0] - 0.001, coords[1] - 0.001],
        ]
        
        for lat, lon in zombie_positions:
            folium.Marker(
                [lat, lon],
                icon=folium.DivIcon(html='<div style="font-size:18px;text-shadow:1px 1px 2px black;">🧟</div>'),
                popup="Zombie threat",
                tooltip="🧟 Infected"
            ).add_to(map_obj)
    
    def _add_zone_detailed_markers(self, map_obj, zone):
        """Add detailed markers for a specific zone - YOUR ORIGINAL DETAILED SYSTEM"""
        color_map = {"low": "green", "medium": "orange", "high": "red"}
        marker_color = color_map.get(zone.danger, "red")
        
        # Enhanced zone marker
        folium.Marker(
            zone.coords,
            popup=f"<b>{zone.name}</b><br>{zone.alert}<br>Resources: {', '.join(zone.resources)}",
            icon=folium.Icon(color="red", icon="exclamation-sign")
        ).add_to(map_obj)
        
        # Danger circle
        folium.CircleMarker(
            location=zone.coords,
            radius=40,
            color=marker_color,
            fill=True,
            fill_opacity=0.3,
            weight=2
        ).add_to(map_obj)
    
    def _add_resource_markers(self, map_obj, zone):
        """Add resource markers based on zone characteristics - YOUR ORIGINAL RESOURCE PLACEMENT"""
        coords = zone.coords
        
        if zone.danger == "low":  # Zone A - High resources
            positions = [
                [coords[0] + 0.001, coords[1] - 0.001, "💧"],
                [coords[0] - 0.002, coords[1] + 0.003, "💧"],
                [coords[0] + 0.003, coords[1] + 0.002, "💧"],
                [coords[0] + 0.002, coords[1] - 0.003, "🍞"],
                [coords[0] - 0.003, coords[1] - 0.001, "🍞"],
                [coords[0] + 0.002, coords[1] + 0.002, "🏠"],
                [coords[0] - 0.002, coords[1] - 0.002, "🏠"],
            ]
        elif zone.danger == "medium":  # Zone B - Medium resources
            positions = [
                [coords[0] + 0.002, coords[1] - 0.002, "💊"],
                [coords[0] - 0.003, coords[1] + 0.002, "💊"],
                [coords[0] + 0.001, coords[1] + 0.003, "🔦"],
                [coords[0] - 0.002, coords[1] - 0.003, "🔦"],
            ]
        else:  # Zone C - Low resources (high risk, high reward)
            positions = [
                [coords[0] + 0.001, coords[1] - 0.002, "🔫"],
                [coords[0] - 0.002, coords[1] + 0.001, "🔫"],
                [coords[0] + 0.003, coords[1] + 0.002, "🩺"],
            ]
        
        for lat, lon, emoji in positions:
            folium.Marker(
                [lat, lon],
                icon=folium.DivIcon(html=f"""
                <div style="
                    font-size: 16px;
                    text-shadow: 1px 1px 3px black;
                    background: rgba(0,0,0,0.7);
                    border-radius: 50%;
                    padding: 4px;
                    border: 1px solid #daa520;
                ">
                {emoji}
                </div>
                """),
                popup=f"<b>📦 Resource</b><br>Zone: {zone.name}<br>Type: {emoji}",
                tooltip=f"{emoji} Resource"
            ).add_to(map_obj)
    
    def _add_zombie_markers(self, map_obj, zone):
        """Add zombie markers based on zone danger level - YOUR ORIGINAL ZOMBIE DISTRIBUTION"""
        coords = zone.coords
        
        if zone.danger == "low":
            zombie_positions = []  # No zombies in safe zones
        elif zone.danger == "medium":
            zombie_positions = [
                [coords[0] + 0.003, coords[1] - 0.003],
                [coords[0] - 0.003, coords[1] + 0.003],
                [coords[0] + 0.005, coords[1] + 0.002],
                [coords[0] - 0.002, coords[1] - 0.005]
            ]
        else:  # high danger
            zombie_positions = [
                [coords[0] + 0.003, coords[1] - 0.003],
                [coords[0] - 0.003, coords[1] + 0.003],
                [coords[0] + 0.005, coords[1] + 0.002],
                [coords[0] - 0.002, coords[1] - 0.005],
                [coords[0] + 0.001, coords[1] + 0.006],
                [coords[0] - 0.006, coords[1] - 0.001],
                [coords[0] + 0.004, coords[1] - 0.001],
                [coords[0] - 0.001, coords[1] + 0.004],
            ]
        
        for lat, lon in zombie_positions:
            folium.Marker(
                [lat, lon],
                icon=folium.DivIcon(html='<div style="font-size:20px;text-shadow:1px 1px 2px black;">🧟</div>'),
                popup=f"Zombie threat in {zone.name}",
                tooltip="🧟 Infected"
            ).add_to(map_obj)
    
    def _add_danger_indicators(self, map_obj, zone):
        """Add danger warning indicators around the zone - YOUR ORIGINAL DANGER SYSTEM"""
        coords = zone.coords
        
        danger_positions = [
            [coords[0] + 0.005, coords[1] + 0.005],
            [coords[0] - 0.005, coords[1] - 0.005]
        ]
        
        for lat, lon in danger_positions:
            folium.Marker(
                [lat, lon],
                icon=folium.DivIcon(html='<div style="font-size:24px;color:red;text-shadow:2px 2px 4px black;">❗</div>'),
                popup="Danger Zone Warning",
                tooltip="⚠️ Danger"
            ).add_to(map_obj)
    
    def _add_cinematic_effects(self, map_html: str, zone) -> str:
        """Add cinematic JavaScript effects to the map - YOUR ORIGINAL CINEMATIC SYSTEM"""
        coords = zone.coords
        
        cinematic_js = f"""
        <script>
        setTimeout(function() {{
            var mapElement = document.querySelector('.folium-map');
            if (mapElement && mapElement._leaflet_map) {{
                var map = mapElement._leaflet_map;
                
                // Cinematic zoom with smooth animation
                map.flyTo([{coords[0]}, {coords[1]}], 18, {{
                    animate: true,
                    duration: 2.5,
                    easeLinearity: 0.1
                }});
                
                // Add tilt effect (pseudo-3D)
                setTimeout(function() {{
                    var mapContainer = map.getContainer();
                    mapContainer.style.transform = 'perspective(1000px) rotateX(15deg)';
                    mapContainer.style.transformOrigin = 'center bottom';
                    mapContainer.style.transition = 'transform 1s ease-out';
                    mapContainer.style.filter = 'contrast(1.1) saturate(1.2)';
                    mapContainer.style.boxShadow = 'inset 0 0 50px rgba(255,0,0,0.1)';
                }}, 1000);
                
                // Reset tilt after viewing
                setTimeout(function() {{
                    var mapContainer = map.getContainer();
                    mapContainer.style.transform = 'perspective(1000px) rotateX(5deg)';
                }}, 4000);
            }}
        }}, 500);
        </script>
        """
        
        return map_html.replace('</div></body>', cinematic_js + '</div></body>')
    
    def _get_fallback_map_html(self, message: str) -> str:
        """Generate fallback HTML when map generation fails."""
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
                🔧 Install dependencies: pip install folium
            </div>
        </div>
        """