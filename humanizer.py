import random
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import wordnet
import string

try:
    nltk.download('punkt', quiet=True)
    nltk.download('wordnet', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)
except Exception as e:
    print(f"NLTK download warning: {e}")

class AdvancedHumanizer:
    def __init__(self):
        self.synonym_cache = {}
        self.phrase_map = {
            "Moreover": ["Furthermore", "In addition", "Besides", "Likewise", "Also"],
            "Additionally": ["Furthermore", "Moreover", "Plus", "In addition", "Besides"],
            "Furthermore": ["Moreover", "Also", "In addition", "Besides", "And"],
            "However": ["Nonetheless", "Nevertheless", "Yet", "Still", "Conversely"],
            "Therefore": ["Thus", "Hence", "Consequently", "As a result", "For that reason"],
            "Dividing": ["Segmenting", "Partitioning", "Splitting", "Separating", "Categorizing"],
            "Selecting": ["Choosing", "Identifying", "Picking", "Determining", "Targeting"],
            "Establishing": ["Creating", "Defining", "Building", "Forming", "Setting up"],
            "visualize": ["illustrate", "depict", "represent", "demonstrate", "show"]
        }
        self.connectors = ["For instance", "Specifically", "In contrast", "Indeed", "Alternatively"]

    def get_synonym(self, word, pos=None):
        if word in self.synonym_cache:
            return self.synonym_cache[word]
        if word in self.phrase_map:
            chosen = random.choice(self.phrase_map[word])
            self.synonym_cache[word] = [chosen]
            return chosen, [word] if chosen != word else []
        try:
            synonyms = []
            for syn in wordnet.synsets(word):
                for lemma in syn.lemmas():
                    synonym = lemma.name().replace("_", " ")
                    if synonym != word and synonym.lower() not in string.punctuation:
                        synonyms.append(synonym)
            self.synonym_cache[word] = synonyms[:5] or [word]
            chosen = random.choice(self.synonym_cache[word]) if synonyms else word
            return chosen, [word] if chosen != word else []
        except Exception as e:
            print(f"Error getting synonyms: {e}")
            return word, []

    def _safe_tokenize(self, text):
        try:
            return word_tokenize(text)
        except Exception:
            return text.split()

    def _safe_sent_tokenize(self, text):
        try:
            return sent_tokenize(text)
        except Exception:
            return [s.strip() for s in text.split('.') if s.strip()]

    def paraphrase_sentence(self, sentence):
        try:
            original = sentence.strip()
            if not original:
                return original, []
            words = self._safe_tokenize(original)
            changes = []

            # Replace key phrases
            for phrase, alternatives in self.phrase_map.items():
                if phrase in sentence:
                    choice = random.choice(alternatives)
                    sentence = sentence.replace(phrase, choice)
                    changes.append(phrase)

            # Synonym substitution
            new_words = []
            pos_tags = nltk.pos_tag(words) if nltk.pos_tag else [(w, 'NN') for w in words]  # Fallback POS
            for word, pos in pos_tags:
                if random.random() < 0.9:  # High chance for change
                    new_word, word_changes = self.get_synonym(word, pos)
                    new_words.append(new_word)
                    changes.extend(word_changes)
                else:
                    new_words.append(word)
            sentence = " ".join(new_words)

            # Shuffle structure
            if len(new_words) > 2:
                shuffled_words = new_words.copy()
                random.shuffle(shuffled_words)
                sentence = " ".join(shuffled_words)
                changes.extend([w for w in words if w not in shuffled_words or words.index(w) != shuffled_words.index(w)])

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
            sentences = self._safe_sent_tokenize(ai_text)
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