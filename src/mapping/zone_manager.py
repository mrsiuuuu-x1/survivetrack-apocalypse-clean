"""
Zone Management System for SurviveTrack
Manages zone data, resource information, and tactical intelligence.
"""

import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

@dataclass
class Zone:
    """Zone data structure with all tactical information."""
    name: str
    coords: List[float]
    resources: List[str]
    alert: str
    danger: str
    description: str
    history: str
    threats: str
    tactical_notes: str
    resource_density: str

class ZoneManager:
    """Manages all zone data and resource information for SurviveTrack."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._initialize_zones()
        self._initialize_resource_markers()
        self.logger.info("🗺️ Zone Manager initialized with 3 tactical zones")
    
    def _initialize_zones(self) -> None:
        """Initialize zone data - THIS IS YOUR ORIGINAL ZONE_DATA FROM main.py"""
        self.zones = {
            "Zone A": Zone(
                name="📍 Zone A – Boat Basin",
                coords=[24.8182, 67.0256],
                resources=["💧 Water", "🍞 Food", "🏠 Shelter"],
                alert="🟢 Clear. No zombies spotted.",
                danger="low",
                description="Former luxury marina district, now a safe haven with abundant fresh water from underground springs and well-stocked food supplies from abandoned restaurants.",
                history="Twenty years ago, this was where the wealthy evacuated first. Their abandoned yachts still hold valuable supplies.",
                threats="Minimal zombie activity, but beware of other survivor groups who may be territorial.",
                tactical_notes="High ground advantage, multiple escape routes via water, natural barriers.",
                resource_density="high"
            ),
            "Zone B": Zone(
                name="📍 Zone B – Lyari",
                coords=[24.8784, 67.0103],
                resources=["💊 Medicine", "🔦 Flashlight"],
                alert="🧟‍♂ Danger! Zombie activity nearby. 🚨",
                danger="medium",
                description="Dense urban area with narrow streets. Former gang territory turned into a medical supply cache after the outbreak.",
                history="The gangs initially fought the infected but were overwhelmed. Their abandoned clinics contain rare medical supplies.",
                threats="Regular zombie patrols, unstable buildings, potential for being trapped in narrow alleys.",
                tactical_notes="Urban warfare environment, requires stealth, multiple entry/exit points compromised.",
                resource_density="medium"
            ),
            "Zone C": Zone(
                name="📍 Zone C – Gillani Railway Station",
                coords=[24.9090, 67.0940],
                resources=["🔫 Weapons", "🩺 Medical Kit"],
                alert="🔴 Safe for now, but stay alert. 👀",
                danger="high",
                description="Major transportation hub converted into a military outpost during the initial outbreak. Contains high-value military equipment.",
                history="Last military holdout in Karachi. Fell after a three-week siege. Weapon caches remain locked in underground bunkers.",
                threats="Heavy zombie concentration, military-grade infected (former soldiers), booby traps in bunkers.",
                tactical_notes="High-risk, high-reward. Recommend full squad deployment with heavy weapons.",
                resource_density="low"
            )
        }
    
    def _initialize_resource_markers(self) -> None:
        """Initialize resource marker definitions - YOUR ORIGINAL RESOURCE_MARKERS"""
        self.resource_markers = {
            "water": {"emoji": "💧", "color": "#4A90E2", "name": "Water Source"},
            "food": {"emoji": "🍞", "color": "#8B4513", "name": "Food Cache"},
            "shelter": {"emoji": "🏠", "color": "#228B22", "name": "Safe Shelter"},
            "medicine": {"emoji": "💊", "color": "#DC143C", "name": "Medical Supplies"},
            "flashlight": {"emoji": "🔦", "color": "#FFD700", "name": "Equipment"},
            "weapons": {"emoji": "🔫", "color": "#696969", "name": "Weapon Cache"},
            "medical_kit": {"emoji": "🩺", "color": "#FF6347", "name": "Medical Kit"},
            "fuel": {"emoji": "⛽", "color": "#FF4500", "name": "Fuel Depot"},
            "ammo": {"emoji": "🎯", "color": "#A0522D", "name": "Ammunition"},
            "radio": {"emoji": "📻", "color": "#9370DB", "name": "Communication"},
            "battery": {"emoji": "🔋", "color": "#00CED1", "name": "Power Source"},
            "tools": {"emoji": "🔧", "color": "#B8860B", "name": "Tools & Parts"}
        }
    
    def get_zone(self, zone_key: str) -> Optional[Zone]:
        """Get zone data by key."""
        return self.zones.get(zone_key)
    
    def get_all_zones(self) -> Dict[str, Zone]:
        """Get all zone data."""
        return self.zones.copy()
    
    def get_resource_marker(self, resource_type: str):
        """Get resource marker information."""
        return self.resource_markers.get(resource_type)
    
    def validate_zone_data(self) -> bool:
        """Validate zone data integrity."""
        try:
            for zone_key, zone in self.zones.items():
                if not all([zone.name, zone.coords, zone.alert, zone.danger]):
                    self.logger.error(f"Missing required fields in {zone_key}")
                    return False
                
                if len(zone.coords) != 2:
                    self.logger.error(f"Invalid coordinates in {zone_key}")
                    return False
                
                if zone.danger not in ["low", "medium", "high"]:
                    self.logger.error(f"Invalid danger level in {zone_key}: {zone.danger}")
                    return False
            
            self.logger.info("✅ Zone data validation passed")
            return True
            
        except Exception as e:
            self.logger.error(f"Zone data validation failed: {e}")
            return False