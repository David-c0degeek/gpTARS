# tars/core/persona_manager.py
import json
import os

class PersonaManager:
    def __init__(self, persona_file="tars_persona.json"):
        self.persona_data = {}
        if os.path.exists(persona_file):
            with open(persona_file, "r", encoding="utf-8") as f:
                self.persona_data = json.load(f)
        else:
            raise FileNotFoundError(f"{persona_file} not found!")
    
    def build_persona_prompt(self, user_text: str) -> str:
        """
        Build a prompt that merges TARS's scenario, personality, 
        traits, and the user's latest query into a single TARS-like prompt.
        """
        name = self.persona_data.get("name", "TARS")
        char_persona = self.persona_data.get("char_persona", "")
        world_scenario = self.persona_data.get("world_scenario", "")
        
        # Gather trait data (if any)
        traits = self.persona_data.get("traits", {})
        
        # Convert trait dictionary into a bullet-point style description:
        traits_str = "\n".join(
            [f"- {trait}: {value}%" for trait, value in traits.items()]
        )
        
        # Build a structured preamble about TARS's personality:
        persona_intro = (
            f"Name: {name}\n"
            f"Persona: {char_persona}\n"
            f"Scenario: {world_scenario}\n\n"
            "Your personality traits:\n"
            f"{traits_str}\n\n"
        )

        # The user's message:
        user_section = f"User: {user_text}\n"

        # The role request for TARS:
        request = (
            "Reply as TARS, showcasing the above traits. "
            "Focus on high Humor, high Sarcasm, but remain disciplined and honest. "
            "Use a witty, slightly sarcastic tone.\n"
        )

        prompt = f"{persona_intro}{user_section}{request}TARS's response:\n"

        return prompt
