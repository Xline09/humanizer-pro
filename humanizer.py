import random
import re
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import wordnet, stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import string
import difflib

try:
    nltk.download('punkt', quiet=True)
    nltk.download('wordnet', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('vader_lexicon', quiet=True)
    nltk.download('punkt_tab', quiet=True)
except Exception as e:
    print(f"NLTK download warning: {e}")

class AdvancedHumanizer:
    def __init__(self):
        self.synonym_cache = {}
        self.common_ai_phrases = {
            "Moreover": ["Also", "Besides", "In addition", "Furthermore", "As well"],
            "Additionally": ["Furthermore", "Also", "In addition", "Plus", "Likewise"],
            "Furthermore": ["Moreover", "Also", "In addition", "Besides", "And"],
            "However": ["But", "Yet", "Nonetheless", "Nevertheless", "Still"],
            "Therefore": ["So", "Thus", "Hence", "As a result", "Consequently"]
        }
        self.human_phrases = {
            "casual": ["in my opinion", "as I see it", "indeed"],
            "formal": ["in my view", "it appears", "evidently"],
            "mixed": ["to be frank", "in practice", "effectively"]
        }
        self.slang = {}  # Removed for formality
        self.punctuation_variations = ['.', '?']
        self.emoticons = []  # Removed for formality
        self.typos = {}  # Removed for formality
        self.stop_words = set(stopwords.words('english'))
        try:
            self.sentiment_analyzer = SentimentIntensityAnalyzer()
        except Exception as e:
            print(f"Failed to initialize SentimentIntensityAnalyzer: {e}")
            self.sentiment_analyzer = None

        self.personal_touches = [
            "from my observations", "based on my analysis", "in my experience"
        ]

    def detect_tone(self, text):
        try:
            if self.sentiment_analyzer is None:
                return "mixed"
            sentiment = self.sentiment_analyzer.polarity_scores(text)
            if sentiment['compound'] > 0.5:
                return "positive"
            elif sentiment['compound'] < -0.5:
                return "negative"
            formal_keywords = ["research", "study", "analysis", "therefore", "however"]
            casual_keywords = ["cool", "nice", "fun", "easy"]
            if any(kw in text.lower() for kw in formal_keywords):
                return "formal"
            elif any(kw in text.lower() for kw in casual_keywords):
                return "casual"
            return "mixed"
        except Exception as e:
            print(f"Error detecting tone: {e}")
            return "mixed"

    def get_contextual_synonyms(self, word, pos_tag):
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

    def introduce_errors(self, sentence, tone):
        return sentence, []  # No errors for formal output

    def vary_sentence_length(self, sentence, tone):
        try:
            words = self._safe_tokenize(sentence)
            original_words = words.copy()
            if len(words) > 8 and random.random() < 0.8:  # Increased chance
                split_point = random.randint(4, len(words) - 1)
                words = words[:split_point]
            elif len(words) < 6 and random.random() < 0.6:
                words.extend(random.choice(self.human_phrases.get(tone, self.human_phrases["mixed"])).split())
            changed = words != original_words
            return " ".join(words), [w for w in original_words if w not in words] if changed else []
        except Exception as e:
            print(f"Error varying sentence length: {e}")
            return sentence, []

    def replace_ai_phrases(self, sentence, tone):
        try:
            original = sentence
            changes = []
            for ai_phrase, alternatives in self.common_ai_phrases.items():
                if ai_phrase in sentence:
                    choice = random.choice(alternatives)
                    if choice != ai_phrase:
                        changes.append(ai_phrase)
                    sentence = sentence.replace(ai_phrase, choice)
            return sentence, changes if sentence != original else []
        except Exception as e:
            print(f"Error replacing AI phrases: {e}")
            return sentence, []

    def add_human_touch(self, sentence, tone):
        try:
            original = sentence
            changes = []
            if random.random() < 0.7:  # Increased chance for change
                insert_pos = random.randint(0, len(sentence.split()))
                words = sentence.split()
                phrase_set = self.human_phrases.get(tone, self.human_phrases["mixed"])
                phrase = random.choice(phrase_set)
                words.insert(insert_pos, phrase)
                changes.append(phrase)
                sentence = " ".join(words)
            if random.random() < 0.3:  # Increased personal touch
                touch = random.choice(self.personal_touches)
                sentence = f"{touch}, {sentence}"
                changes.append(touch)
            return sentence, changes if sentence != original else []
        except Exception as e:
            print(f"Error adding human touch: {e}")
            return sentence, []

    def restructure_sentence(self, sentence):
        try:
            words = self._safe_tokenize(sentence)
            original_words = words.copy()
            if len(words) > 6 and random.random() < 0.8:  # Increased chance
                try:
                    pos_tags = nltk.pos_tag(words)
                    nouns = [word for word, pos in pos_tags if pos.startswith('NN')]
                    verbs = [word for word, pos in pos_tags if pos.startswith('VB')]
                    if nouns and verbs:
                        new_order = []
                        new_order.extend(random.sample(nouns, min(2, len(nouns))))
                        new_order.extend(random.sample(verbs, min(1, len(verbs))))
                        remaining = [w for w in words if w not in nouns and w not in verbs]
                        random.shuffle(remaining)
                        new_order.extend(remaining)
                        sentence = " ".join(new_order)
                        return sentence, [w for w in original_words if w not in new_order or original_words.index(w) != new_order.index(w)]
                except Exception as e:
                    print(f"Error in POS tagging: {e}")
            return sentence, []
        except Exception as e:
            print(f"Error restructuring sentence: {e}")
            return sentence, []

    def adjust_tone(self, sentence, original_tone):
        try:
            original = sentence
            changes = []
            if original_tone == "formal" and random.random() < 0.6:  # Increased chance
                if re.search(r'\bis\b', sentence):
                    sentence = re.sub(r'\bis\b', "appears to be", sentence, 1)
                    changes.append("is → appears to be")
            return sentence, changes
        except Exception as e:
            print(f"Error adjusting tone: {e}")
            return sentence, []

    def can_tokenize(self):
        try:
            sent_tokenize("test")
            return True
        except LookupError:
            return False

    def _safe_tokenize(self, text):
        try:
            if self.can_tokenize():
                return word_tokenize(text)
            else:
                return text.split()
        except Exception as e:
            print(f"Error in tokenization: {e}")
            return text.split()

    def humanize(self, ai_text):
        try:
            if not ai_text.strip():
                return "No text provided to humanize.", []
            if self.can_tokenize():
                sentences = sent_tokenize(ai_text)
            else:
                sentences = [s.strip() for s in ai_text.split('.') if s.strip()]
            tone = self.detect_tone(ai_text) if self.sentiment_analyzer else "mixed"
            humanized_sentences = []
            all_changes = []

            for sentence in sentences:
                if not sentence:
                    continue
                try:
                    original = sentence
                    sentence_changes = []
                    # Ensure at least one change per sentence
                    sentence, changes = self.replace_ai_phrases(sentence, tone)
                    sentence_changes.extend(changes)
                    sentence, changes = self.vary_sentence_length(sentence, tone)
                    sentence_changes.extend(changes)
                    sentence, changes = self.restructure_sentence(sentence)
                    sentence_changes.extend(changes)
                    sentence, changes = self.add_human_touch(sentence, tone)
                    sentence_changes.extend(changes)
                    sentence, changes = self.adjust_tone(sentence, tone)
                    sentence_changes.extend(changes)
                    humanized_sentences.append(sentence)
                    if sentence != original:
                        all_changes.extend(sentence_changes)
                except Exception as e:
                    print(f"Error processing sentence '{sentence}': {e}")
                    humanized_sentences.append(sentence)

            final_text = " ".join(humanized_sentences).strip()
            if not final_text:
                return "Humanization resulted in no output. Original text returned.", []
            return final_text, list(set(all_changes))
        except Exception as e:
            print(f"Critical error in humanization: {e}")
            return f"Cannot humanize: {str(e)}. Original text: {ai_text}", []