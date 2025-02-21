import random
import re
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import wordnet, stopwords
import string

try:
    nltk.download('punkt', quiet=True)
    nltk.download('wordnet', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)
    nltk.download('stopwords', quiet=True)
except Exception as e:
    print(f"NLTK download warning: {e}")

class AdvancedHumanizer:
    def __init__(self):
        self.synonym_cache = {}
        self.common_ai_phrases = {
            "Moreover": ["Furthermore", "In addition", "Additionally", "Besides", "Likewise"],
            "Additionally": ["Furthermore", "Also", "Moreover", "In addition", "Plus"],
            "Furthermore": ["Moreover", "In addition", "Besides", "Also", "And"],
            "However": ["Nonetheless", "Nevertheless", "Yet", "Still", "Conversely"],
            "Therefore": ["Thus", "Hence", "Consequently", "As a result", "For that reason"]
        }
        self.connectors = ["For instance", "Specifically", "In contrast", "Indeed", "Alternatively"]
        self.stop_words = set(stopwords.words('english'))

    def get_synonym(self, word, pos_tag):
        if word in self.synonym_cache:
            return self.synonym_cache[word]
        try:
            synonyms = []
            for syn in wordnet.synsets(word):
                if pos_tag.startswith('NN') and syn.pos() == 'n':
                    for lemma in syn.lemmas():
                        synonym = lemma.name().replace("_", " ")
                        if synonym != word and synonym.lower() not in string.punctuation and synonym.lower() not in self.stop_words:
                            synonyms.append(synonym)
                elif pos_tag.startswith('VB') and syn.pos() == 'v':
                    for lemma in syn.lemmas():
                        synonym = lemma.name().replace("_", " ")
                        if synonym != word and synonym.lower() not in string.punctuation and synonym.lower() not in self.stop_words:
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
        except Exception as e:
            print(f"Error in tokenization: {e}")
            return text.split()

    def _safe_sent_tokenize(self, text):
        try:
            return sent_tokenize(text)
        except Exception as e:
            print(f"Error in sentence tokenization: {e}")
            return [s.strip() for s in text.split('.') if s.strip()]

    def paraphrase_sentence(self, sentence):
        try:
            original = sentence.strip()
            if not original:
                return original, []
            words = self._safe_tokenize(original)
            pos_tags = nltk.pos_tag(words)
            changes = []

            # Replace common AI phrases
            for ai_phrase, alternatives in self.common_ai_phrases.items():
                if ai_phrase in sentence:
                    choice = random.choice(alternatives)
                    sentence = sentence.replace(ai_phrase, choice)
                    changes.append(ai_phrase)

            # Synonym substitution for content words
            new_words = []
            for word, pos in pos_tags:
                if word.lower() not in self.stop_words and random.random() < 0.9:  # High chance for change
                    new_word, word_changes = self.get_synonym(word, pos)
                    new_words.append(new_word)
                    changes.extend(word_changes)
                else:
                    new_words.append(word)
            sentence = " ".join(new_words)

            # Restructure sentence (simplified for reliability)
            if len(words) > 2:
                shuffled_words = new_words.copy()
                random.shuffle(shuffled_words)
                sentence = " ".join(shuffled_words)
                changes.extend([w for w in words if w not in shuffled_words or words.index(w) != shuffled_words.index(w)])

            # Add connector for variation
            connector = random.choice(self.connectors)
            sentence = f"{connector}, {sentence.lower()}"
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