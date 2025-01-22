# tars/main.py

import yaml
from core.stt_engine import STTEngine
from core.tts_engine import TTSEngine
from core.llm_integration import OpenAIEngine, AnthropicEngine, LocalLlamaEngine
from core.tars_core import TARSCore
from core.persona_manager import PersonaManager


def main():
    # 1. Load config
    with open("tars/config/config.yaml", "r") as f:
        config = yaml.safe_load(f)

    # 2. Initialize Persona
    persona_manager = PersonaManager("tars/tars_persona.json")

    # 3. Initialize STT & TTS
    stt = STTEngine(config)
    tts = TTSEngine(config)

    # 4. Decide which LLM engine to use
    engine_type = config['llm']['engine']  # "openai", "anthropic", or "local"

    if engine_type == "openai":
        llm_fast = OpenAIEngine(config, mode="fast")
        llm_heavy = OpenAIEngine(config, mode="heavy")
    elif engine_type == "anthropic":
        llm_fast = AnthropicEngine(config, mode="fast")
        llm_heavy = AnthropicEngine(config, mode="heavy")
    else:  # "local"
        llm_fast = LocalLlamaEngine(config, mode="fast")
        llm_heavy = LocalLlamaEngine(config, mode="heavy")

    # 5. Initialize TARS Core
    tars_core = TARSCore(
        stt=stt,
        tts=tts,
        llm_fast=llm_fast,
        llm_heavy=llm_heavy,
        persona_manager=persona_manager,
        config=config
    )

    # 6. Start listening
    def stt_callback(transcribed_text):
        tars_core.process_audio_text(transcribed_text)

    print("TARS is running. Say: 'Hey TARS?' to wake.")
    stt.start_listening(stt_callback)


if __name__ == "__main__":
    main()
