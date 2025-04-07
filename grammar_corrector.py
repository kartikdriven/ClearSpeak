# grammar_corrector.py

from transformers import T5Tokenizer, T5ForConditionalGeneration

class GrammarCorrector:
    def __init__(self):
        print("🔧 Loading grammar correction model...")
        self.tokenizer = T5Tokenizer.from_pretrained("vennify/t5-base-grammar-correction")
        self.model = T5ForConditionalGeneration.from_pretrained("vennify/t5-base-grammar-correction")
        print("✅ Grammar correction model loaded.")

    def correct_grammar(self, text):
        input_text = "correct: " + text
        input_ids = self.tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)

        outputs = self.model.generate(input_ids, max_length=512, num_beams=4, early_stopping=True)

        corrected_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return corrected_text
