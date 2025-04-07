# speech_synthesis.py

from TTS.api import TTS
import tempfile
import os

class SpeechSynthesizer:
    def __init__(self):
        self.tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False, gpu=False)

    def speak(self, text):
    # Create temporary WAV file and play it
     with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        self.tts.tts_to_file(text=text, file_path=f.name)
        print(f"🗣️ Speaking: {text}")
        os.startfile(f.name)  # For Windows only

