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
            "Dividing": ["Segmenting", "Partitioning", "Separating", "Categorizing", "Splitting"],
            "Selecting": ["Choosing", "Identifying", "Picking", "Determining", "Targeting"],
            "Establishing": ["Creating", "Defining", "Building", "Forming", "Setting"],
            "visualize": ["illustrate", "depict", "represent", "demonstrate", "portray"],
            "based on": ["grounded in", "relying on", "derived from", "built upon", "drawn from"],
            "groups": ["categories", "clusters", "segments", "classes", "collections"],
            "common": ["shared", "similar", "mutual", "typical", "standard"],
            "characteristics": ["traits", "features", "attributes", "properties", "qualities"],
            "serve": ["address", "target", "support", "assist", "cater to"],
            "Strategies": ["Approaches", "Methods", "Techniques", "Plans", "Tactics"],
            "ranging": ["spanning", "varying", "extending", "covering", "stretching"],
            "image": ["identity", "perception", "reputation", "profile", "impression"],
            "mind": ["perception", "thoughts", "awareness", "consciousness", "view"],
            "consumer": ["customer", "buyer", "user", "client", "individual"],
            "tool": ["instrument", "resource", "method", "device", "means"],
            "used": ["employed", "utilized", "applied", "implemented", "adopted"],
            "distinct": ["unique", "separate", "specific", "different", "individual"],
            "market": ["marketplace", "sector", "industry", "field", "arena"],
            "into": ["within", "across", "among", "throughout", "inside"]
        }
        self.connectors = ["For example", "In particular", "On the contrary", "Notably", "Conversely"]

    def get_synonym(self, word):
        word_lower = word.lower()
        if word_lower in self.phrase_map:
            choice = random.choice(self.phrase_map[word_lower])
            return choice, [word] if choice.lower() != word_lower else []
        return word, []

    def split_sentences(self, text):
        # Robust sentence splitting without NLTK
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())
        return [s.strip() for s in sentences if s.strip()]

    def paraphrase_sentence(self, sentence):
        try:
            original = sentence.strip()
            if not original:
                return original, []
            words = original.split()
            changes = []

            # Replace phrases and key words
            for phrase, alternatives in self.phrase_map.items():
                if phrase in sentence:
                    choice = random.choice(alternatives)
                    sentence = sentence.replace(phrase, choice)
                    changes.append(phrase)

            # Rewrite with synonyms
            new_words = []
            for word in words:
                if random.random() < 0.95:  # Near-guaranteed change
                    new_word, word_changes = self.get_synonym(word)
                    new_words.append(new_word)
                    changes.extend(word_changes)
                else:
                    new_words.append(word)

            # Reorder clauses (simplified)
            if len(new_words) > 5:
                mid = len(new_words) // 2
                first_half = new_words[:mid]
                second_half = new_words[mid:]
                sentence = " ".join(second_half + first_half)
            else:
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
            sentences = self.split_sentences(ai_text)
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