# voice_bot.py

from custom_speech_recognizer import CustomSpeechRecognizer
from text_analyzer import TextAnalyzer
from feedback_generator import FeedbackGenerator
from speech_synthesis import SpeechSynthesizer
from grammar_corrector import GrammarCorrector 
from speech_synthesis import get_synthesizer

class VoiceBot:
    def __init__(self):
        self.synthesizer = get_synthesizer()  
        self.recognizer = CustomSpeechRecognizer()
        self.corrector = GrammarCorrector()
        self.analyzer = TextAnalyzer()
        self.generator = FeedbackGenerator()


    def process_audio(self, recognized_text):
        if not recognized_text.strip():
            return "", "⚠️ Could not recognize your speech. Please try again.", ""

        print(f"\n🗣️ You said: {recognized_text}")

        # Step 1: Correct grammar
        corrected_text = self.corrector.correct_grammar(recognized_text)
        print(f"\n✏️ Corrected Text: {corrected_text}")

        # Step 2: Analyze the corrected text
        analysis_result = self.analyzer.analyze_text(corrected_text)

        # Step 3: Generate feedback
        feedback = self.generator.generate_feedback(analysis_result)
        print(f"\n💬 Feedback:\n{feedback}")

        # Step 4: Speak out the corrected version
        audio_filename = self.synthesizer.speak(corrected_text)

        return corrected_text, feedback, audio_filename
