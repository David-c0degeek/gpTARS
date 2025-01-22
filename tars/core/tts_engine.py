# tars/core/tts_engine.py

import pyttsx3

class TTSEngine:
    def __init__(self, config):
        self.config = config
        self.tts = pyttsx3.init()
        voice_name = self.config['tts'].get('voice_name')
        if voice_name:
            for voice in self.tts.getProperty('voices'):
                if voice.name == voice_name:
                    self.tts.setProperty('voice', voice.id)
                    break

    def speak(self, text):
        self.tts.say(text)
        self.tts.runAndWait()
