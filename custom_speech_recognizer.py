import speech_recognition as sr
from vosk import Model, KaldiRecognizer
import pyaudio
import json
import os

class CustomSpeechRecognizer:
    def __init__(self, model_path="model"):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        if not os.path.exists(model_path):
            raise Exception(f"Model not found at {model_path}")
        self.model = Model(model_path)

    def recognize_speech(self):
        print("🎤 Say something to analyze your communication skills...")

        # Start audio stream
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
        stream.start_stream()

        rec = KaldiRecognizer(self.model, 16000)

        while True:
            data = stream.read(4096, exception_on_overflow=False)
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result.get("text", "")
                if text:
                    print("🗣️ You said:", text)
                    return text
