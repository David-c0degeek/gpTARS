# tars/core/stt_engine.py

import vosk
import pyaudio
import queue
import threading
import json

class STTEngine:
    def __init__(self, config):
        self.config = config
        # Path to your Vosk model folder (e.g. "tars/core/stt/vosk-model-small-en-us-0.15")
        self.model = vosk.Model("tars/core/stt/vosk-model-small-en-us-0.15")

        # Create a recognizer for 16 kHz audio
        self.recognizer = vosk.KaldiRecognizer(self.model, 16000)

        self.audio_queue = queue.Queue()
        self.running = False
        self.trigger_phrase = "hey tars"
        self.exit_phrase = "tars go sleep"

    def start_listening(self, callback):
        """
        Continuously captures audio, sends chunks to the Vosk recognizer,
        and invokes the callback with transcribed text once recognized.
        """
        self.running = True
        audio_thread = threading.Thread(target=self._capture_audio)
        audio_thread.start()

        while self.running:
            if not self.audio_queue.empty():
                audio_data = self.audio_queue.get()

                # Feed chunk to Vosk
                if self.recognizer.AcceptWaveform(audio_data):
                    # Vosk got a "complete" enough segment
                    result_json = self.recognizer.Result()
                else:
                    # Partial result (speech still in progress)
                    result_json = self.recognizer.PartialResult()

                text = self._extract_text(result_json)
                # Vosk partial results might be empty strings; adapt to your needs:
                if text:
                    callback(text)

    def _capture_audio(self):
        """
        Continuously read 1024 bytes from the microphone and add them to a queue.
        """
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=16000,
                        input=True,
                        frames_per_buffer=1024)
        while self.running:
            data = stream.read(1024, exception_on_overflow=False)
            self.audio_queue.put(data)

        stream.stop_stream()
        stream.close()
        p.terminate()

    def _extract_text(self, result_json):
        """
        Parse the recognized text from Vosk's JSON output.
        For partial results: {"partial": "..."}
        For final results:   {"text": "..."}
        """
        try:
            result_dict = json.loads(result_json)
        except json.JSONDecodeError:
            return ""

        # For final results (AcceptWaveform == True):
        if "text" in result_dict:
            return result_dict["text"].strip().lower()
        # For partial results:
        if "partial" in result_dict:
            return result_dict["partial"].strip().lower()
        return ""

    def stop_listening(self):
        self.running = False
