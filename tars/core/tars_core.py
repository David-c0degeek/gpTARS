# tars/core/tars_core.py

class TARSCore:
    def __init__(self, stt, tts, llm_fast, llm_heavy, persona_manager, config):
        self.stt = stt
        self.tts = tts
        self.llm_fast = llm_fast
        self.llm_heavy = llm_heavy
        self.persona_manager = persona_manager
        self.config = config
        self.listening_mode = False

        # Default to fast engine
        self.current_llm = self.llm_fast

    def process_audio_text(self, text):
        # [Wake/sleep commands as before...]
        if not self.listening_mode:
            return

        # Switch between fast / heavy
        if "activate think mode" in text:
            self.current_llm = self.llm_heavy
            self.tts.speak("Switching to heavy thinking mode.")
            return
        elif "regular mode" in text:
            self.current_llm = self.llm_fast
            self.tts.speak("Fast mode engaged.")
            return

        # Generate response
        prompt = self.persona_manager.build_persona_prompt(user_text=text)
        response = self.current_llm.generate_response(prompt)
        self.tts.speak(response)
