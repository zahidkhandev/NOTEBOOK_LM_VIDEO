"""
Professional video generation service using YAML configuration.
Implements script generation, visual design, timing, and QA from config.
"""

import logging
import yaml
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class ProfessionalVideoService:
    """Generate professional videos following YAML specifications."""
    
    def __init__(self):
        """Load all YAML configurations."""
        self.load_configs()
    
    def load_configs(self):
        """Load all YAML config files - WITH UTF-8 ENCODING."""
        try:
            # Get the path relative to where the service runs
            base_path = Path(__file__).parent.parent.parent / "prompts"
            
            print(f"📂 Loading configs from: {base_path}")
            
            # Channel categories
            with open(base_path / "channel_categories.yaml", encoding='utf-8') as f:
                self.channels = yaml.safe_load(f).get("channel_categories", {})
            
            # Script generation
            with open(base_path / "script_generation.yaml", encoding='utf-8') as f:
                self.script_config = yaml.safe_load(f).get("script_generation", {})
            
            # Content analysis
            with open(base_path / "content_analysis.yaml", encoding='utf-8') as f:
                self.analysis_config = yaml.safe_load(f).get("content_analysis", {})
            
            # Video design
            with open(base_path / "video_design.yaml", encoding='utf-8') as f:
                self.design_config = yaml.safe_load(f).get("video_design", {})
            
            # Pacing & timing
            with open(base_path / "pacing_timing.yaml", encoding='utf-8') as f:
                self.timing_config = yaml.safe_load(f).get("pacing_timing", {})
            
            # Quality assurance
            with open(base_path / "quality_assurance.yaml", encoding='utf-8') as f:
                self.qa_config = yaml.safe_load(f).get("quality_assurance", {})
            
            logger.info(f"✅ All YAML configs loaded from: {base_path}")
        
        except FileNotFoundError as fe:
            logger.error(f"❌ Config file not found: {fe}")
            raise
        except UnicodeDecodeError as ue:
            logger.error(f"❌ UTF-8 Encoding error: {ue}")
            raise
        except Exception as e:
            logger.error(f"❌ Failed to load configs: {e}")
            raise
    
    def get_channel_config(self, channel_id: str) -> Optional[Dict]:
        """Get channel configuration."""
        return self.channels.get(channel_id)
    
    def get_script_guidelines(self) -> Dict:
        """Get script generation guidelines."""
        return self.script_config
    
    def get_design_specs(self, channel_id: str) -> Dict:
        """Get design specifications for channel."""
        return self.design_config.get(channel_id, self.design_config.get("default", {}))
    
    def get_timing_specs(self) -> Dict:
        """Get timing and pacing specifications."""
        return self.timing_config
    
    def get_qa_requirements(self) -> Dict:
        """Get quality assurance requirements."""
        return self.qa_config
    
    async def build_script_prompt(self, title: str, sources: str, channel_id: str) -> str:
        """Build Gemini prompt using script generation config."""
        guidelines = self.script_config.get("guidelines", {})
        
        prompt = f"""Generate a PROFESSIONAL video script following these guidelines:

Title: {title}
Channel: {channel_id}

SCRIPT GUIDELINES:
- Hook: {guidelines.get('hook', 'Engage immediately')}
- Structure: {guidelines.get('structure', 'Clear sections')}
- Tone: {guidelines.get('tone', 'Professional')}
- Pacing: {guidelines.get('pacing', 'Natural rhythm')}

Source Material:
{sources[:2000]}

Output ONLY clean script text, no markdown."""
        
        return prompt
    
    async def build_visual_prompt(self, script: str, channel_id: str) -> str:
        """Build visual generation prompt from design config."""
        design = self.get_design_specs(channel_id)
        
        prompt = f"""Generate CINEMATIC visual frame descriptions:

Design Style: {design.get('style', 'Professional')}
Color Palette: {design.get('colors', 'Professional')}
Animation: {design.get('animation_style', 'Smooth')}
Visual Emphasis: {design.get('visual_emphasis', 'Key concepts')}

Script to visualize:
{script[:1000]}

Generate 15 vivid, cinematic frame descriptions."""
        
        return prompt


def get_professional_video_service() -> ProfessionalVideoService:
    """Get service instance."""
    return ProfessionalVideoService()
