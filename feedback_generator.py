import spacy
import re

class FeedbackGenerator:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        print("🧠 Feedback Generator Initialized")

    def generate(self, original_text, corrected_text):
        analysis_result = self.analyze_text(corrected_text)
        analysis_result['grammar_issues'] = self.detect_issues(original_text, corrected_text)
        return self.generate_feedback(analysis_result)

    def analyze_text(self, text):
        doc = self.nlp(text)
        return {
            "num_sentences": len(list(doc.sents)),
            "num_tokens": len(doc),
            "num_nouns": len([token for token in doc if token.pos_ == "NOUN"]),
            "num_verbs": len([token for token in doc if token.pos_ == "VERB"])
        }

    @staticmethod
    def remove_emojis(text):
        return re.sub(r'[^\w\s,.!?]', '', text)

    def detect_issues(self, original, corrected):
        return [] if original.strip().lower() == corrected.strip().lower() else [f"Try saying: \"{corrected}\" instead of \"{original}\""]

    def generate_feedback(self, analysis_result):
        feedback = [
            f"You spoke {analysis_result['num_sentences']} sentence(s) with {analysis_result['num_tokens']} words.",
            f"I noticed {analysis_result['num_nouns']} nouns and {analysis_result['num_verbs']} verbs in your speech."
        ]

        if analysis_result.get("grammar_issues"):
            feedback.append("Here are some grammar suggestions:")
            feedback.extend([f"- {issue}" for issue in analysis_result["grammar_issues"]])
        else:
            feedback.append("Great job! No major grammar issues detected. 👍")

        return "\n".join(feedback)
