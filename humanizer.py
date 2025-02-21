import random
import re

class AdvancedHumanizer:
    def __init__(self):
        self.phrase_map = {
            "Moreover": ["Furthermore", "In addition", "Besides", "Likewise", "Also"],
            "Additionally": ["Furthermore", "Moreover", "Plus", "In addition", "Besides"],
            "Furthermore": ["Moreover", "In addition", "Besides", "Also", "And"],
            "However": ["Nonetheless", "Nevertheless", "Yet", "Still", "Conversely"],
            "Therefore": ["Thus", "Hence", "Consequently", "As a result", "For that reason"],
            "Dividing": ["Segmenting", "Partitioning", "Splitting", "Separating", "Categorizing"],
            "Selecting": ["Choosing", "Identifying", "Picking", "Determining", "Targeting"],
            "Establishing": ["Creating", "Defining", "Building", "Forming", "Setting up"],
            "visualize": ["illustrate", "depict", "represent", "demonstrate", "show"],
            "based on": ["relying on", "grounded in", "depending on", "built upon", "drawn from"],
            "groups": ["categories", "clusters", "segments", "classes", "divisions"],
            "common": ["shared", "similar", "typical", "mutual", "standard"],
            "characteristics": ["traits", "features", "attributes", "properties", "qualities"],
            "serve": ["address", "target", "cater to", "assist", "support"],
            "Strategies": ["Approaches", "Methods", "Techniques", "Tactics", "Plans"],
            "ranging": ["varying", "spanning", "extending", "covering", "stretching"],
            "image": ["identity", "perception", "reputation", "profile", "impression"],
            "mind": ["perception", "thoughts", "awareness", "view", "consciousness"],
            "consumer": ["customer", "buyer", "individual", "client", "user"],
            "tool": ["instrument", "device", "method", "means", "resource"],
            "used": ["employed", "utilized", "applied", "implemented", "adopted"]
        }
        self.connectors = ["For instance", "Specifically", "In contrast", "Indeed", "Alternatively"]

    def get_synonym(self, word):
        word_lower = word.lower()
        if word_lower in self.phrase_map:
            choice = random.choice(self.phrase_map[word_lower])
            return choice, [word] if choice.lower() != word_lower else []
        return word, []

    def _split_sentences(self, text):
        # Simple sentence splitting without NLTK dependency
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())
        return [s.strip() for s in sentences if s.strip()]

    def paraphrase_sentence(self, sentence):
        try:
            original = sentence.strip()
            if not original:
                return original, []
            words = original.split()
            changes = []

            # Replace key phrases
            for phrase, alternatives in self.phrase_map.items():
                if phrase in sentence:
                    choice = random.choice(alternatives)
                    sentence = sentence.replace(phrase, choice)
                    changes.append(phrase)

            # Synonym substitution
            new_words = []
            for word in words:
                if random.random() < 0.9:  # High chance for change
                    new_word, word_changes = self.get_synonym(word)
                    new_words.append(new_word)
                    changes.extend(word_changes)
                else:
                    new_words.append(word)
            sentence = " ".join(new_words)

            # Add connector
            connector = random.choice(self.connectors)
            sentence = f"{connector}, {sentence}"
            changes.append(connector)

            # Capitalize and punctuate
            sentence = sentence[0].upper() + sentence[1:]
            if not sentence.endswith(('.', '?', '!')):
                sentence += '.'
                changes.append('.')

            return sentence, changes
        except Exception as e:
            print(f"Error paraphrasing sentence '{sentence}': {e}")
            return sentence, []

    def humanize(self, ai_text):
        try:
            if not ai_text.strip():
                return "No text provided to humanize.", []
            sentences = self._split_sentences(ai_text)
            humanized_sentences = []
            all_changes = []

            for sentence in sentences:
                if not sentence:
                    continue
                humanized, changes = self.paraphrase_sentence(sentence)
                humanized_sentences.append(humanized)
                all_changes.extend(changes)

            final_text = " ".join(humanized_sentences).strip()
            if not final_text:
                return "Humanization resulted in no output. Original text returned.", []
            return final_text, list(set(all_changes))
        except Exception as e:
            print(f"Critical error in humanization: {e}")
            return f"Cannot humanize: {str(e)}. Original text: {ai_text}", []