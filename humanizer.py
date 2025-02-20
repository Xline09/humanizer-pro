import random
import re
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import wordnet, stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import string

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
            "Moreover": ["Additionally", "Furthermore", "In addition", "Likewise", "As well"],
            "Additionally": ["Furthermore", "Moreover", "In addition", "Also", "Similarly"],
            "Furthermore": ["Moreover", "Additionally", "In addition", "Likewise", "And"],
            "However": ["Nevertheless", "Nonetheless", "Yet", "Still", "On the other hand"],
            "Therefore": ["Thus", "Hence", "Consequently", "As a result", "For that reason"]
        }
        self.human_phrases = {
            "casual": ["in my opinion", "as observed", "indeed"],  # Subtle, minimal
            "formal": ["in my view", "it appears", "evidently"],
            "mixed": ["to be frank", "essentially", "notably"]
        }
        self.slang = {}  # No slang
        self.punctuation_variations = ['.', '?']  # Formal only
        self.emoticons = []  # No emojis
        self.typos = {}  # No typos
        self.stop_words = set(stopwords.words('english'))
        try:
            self.sentiment_analyzer = SentimentIntensityAnalyzer()
        except Exception as e:
            print(f"Failed to initialize SentimentIntensityAnalyzer: {e}")
            self.sentiment_analyzer = None

        self.personal_touches = [
            "from my analysis", "based on observations", "considering the context"
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
            self.synonym_cache[word] = synonyms[:3] or [word]  # Fewer synonyms for subtlety
            return self.synonym_cache[word]
        except Exception as e:
            print(f"Error getting synonyms: {e}")
            return [word]

    def introduce_errors(self, sentence, tone):
        return sentence  # No errors

    def vary_sentence_length(self, sentence, tone):
        try:
            words = self._safe_tokenize(sentence)
            if len(words) > 12 and random.random() < 0.3:  # Lowered from 0.6
                words = words[:random.randint(6, len(words) // 2)]
            return " ".join(words)
        except Exception as e:
            print(f"Error varying sentence length: {e}")
            return sentence

    def replace_ai_phrases(self, sentence, tone):
        try:
            for ai_phrase, alternatives in self.common_ai_phrases.items():
                if ai_phrase in sentence:
                    sentence = sentence.replace(ai_phrase, random.choice(alternatives))
            return sentence
        except Exception as e:
            print(f"Error replacing AI phrases: {e}")
            return sentence

    def add_human_touch(self, sentence, tone):
        try:
            if random.random() < 0.05:  # Drastically lowered from 0.4/0.2—rare insertion
                insert_pos = random.randint(0, len(sentence.split()))
                words = sentence.split()
                phrase_set = self.human_phrases.get(tone, self.human_phrases["mixed"])
                words.insert(insert_pos, random.choice(phrase_set))
                sentence = " ".join(words)
            if random.random() < 0.02:  # Very rare—mimics Tkinter sparsity
                sentence = random.choice(self.personal_touches) + ", " + sentence
            return sentence
        except Exception as e:
            print(f"Error adding human touch: {e}")
            return sentence

    def restructure_sentence(self, sentence):
        try:
            words = self._safe_tokenize(sentence)
            if len(words) > 10 and random.random() < 0.2:  # Rarer, longer threshold
                try:
                    pos_tags = nltk.pos_tag(words)
                    nouns = [word for word, pos in pos_tags if pos.startswith('NN')]
                    verbs = [word for word, pos in pos_tags if pos.startswith('VB')]
                    if nouns and verbs:
                        new_order = []
                        new_order.extend(random.sample(nouns, min(1, len(nouns))))  # Fewer words
                        new_order.extend(random.sample(verbs, min(1, len(verbs))))
                        remaining = [w for w in words if w not in nouns and w not in verbs]
                        random.shuffle(remaining)
                        new_order.extend(remaining)
                        return " ".join(new_order)
                except Exception as e:
                    print(f"Error in POS tagging: {e}")
            return sentence
        except Exception as e:
            print(f"Error restructuring sentence: {e}")
            return sentence

    def adjust_tone(self, sentence, original_tone):
        try:
            if original_tone == "formal":
                if random.random() < 0.1:  # Subtle tweak
                    sentence = re.sub(r'\bis\b', "appears to be", sentence, 1)
            return sentence
        except Exception as e:
            print(f"Error adjusting tone: {e}")
            return sentence

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
                return "No text provided to humanize."
            if self.can_tokenize():
                sentences = sent_tokenize(ai_text)
            else:
                sentences = [s.strip() for s in ai_text.split('.') if s.strip()]
            tone = self.detect_tone(ai_text) if self.sentiment_analyzer else "mixed"
            humanized_sentences = []
            for sentence in sentences:
                if not sentence:
                    continue
                try:
                    sentence = self.replace_ai_phrases(sentence, tone)
                    sentence = self.vary_sentence_length(sentence, tone)
                    sentence = self.restructure_sentence(sentence)
                    sentence = self.add_human_touch(sentence, tone)
                    sentence = self.adjust_tone(sentence, tone)
                    humanized_sentences.append(sentence)
                except Exception as e:
                    print(f"Error processing sentence '{sentence}': {e}")
                    humanized_sentences.append(sentence)
            final_text = " ".join(humanized_sentences).strip()
            if not final_text:
                return "Humanization resulted in no output. Original text returned."
            return final_text
        except Exception as e:
            print(f"Critical error in humanization: {e}")
            return f"Cannot humanize: {str(e)}. Original text: {ai_text}"