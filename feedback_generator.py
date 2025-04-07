# feedback_generator.py

class FeedbackGenerator:
    def generate_feedback(self, analysis_result):
        feedback = []

        feedback.append(f"You spoke {analysis_result['num_sentences']} sentence(s) with {analysis_result['num_tokens']} words.")
        feedback.append(f"I noticed {analysis_result['num_nouns']} nouns and {analysis_result['num_verbs']} verbs in your speech.")

        if analysis_result["grammar_issues"]:
            feedback.append("Here are some grammar suggestions:")
            for issue in analysis_result["grammar_issues"]:
                feedback.append(f"- {issue}")
        else:
            feedback.append("Great job! No major grammar issues detected. 👍")

        return "\n".join(feedback)
