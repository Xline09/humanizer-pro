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
            "Moreover": ["Furthermore", "In addition", "Additionally", "Besides", "Likewise"],
            "Additionally": ["Furthermore", "Also", "Moreover", "In addition", "Plus"],
            "Furthermore": ["Moreover", "In addition", "Besides", "Also", "And"],
            "However": ["Nonetheless", "Nevertheless", "Yet", "Still", "Conversely"],
            "Therefore": ["Thus", "Hence", "Consequently", "As a result", "For that reason"]
        }
        self.connectors = ["For instance", "Specifically", "In contrast", "Indeed", "On the contrary"]
        self.stop_words = set(stopwords.words('english'))
        try:
            self.sentiment_analyzer = SentimentIntensityAnalyzer()
        except Exception as e:
            print(f"Failed to initialize SentimentIntensityAnalyzer: {e}")
            self.sentiment_analyzer = None

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

    def paraphrase_sentence(self, sentence, tone):
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
                    if choice != ai_phrase:
                        changes.append(ai_phrase)
                    sentence = sentence.replace(ai_phrase, choice)

            # Synonym substitution for key words
            new_words = []
            for word, pos in pos_tags:
                if random.random() < 0.85 and word.lower() not in self.stop_words:  # High chance for change
                    new_word, word_changes = self.get_synonym(word, pos)
                    new_words.append(new_word)
                    changes.extend(word_changes)
                else:
                    new_words.append(word)
            sentence = " ".join(new_words)

            # Restructure sentence
            if len(words) > 3:  # Apply to shorter sentences
                pos_tags = nltk.pos_tag(self._safe_tokenize(sentence))
                nouns = [w for w, p in pos_tags if p.startswith('NN')]
                verbs = [w for w, p in pos_tags if p.startswith('VB')]
                if nouns and verbs and random.random() < 0.95:  # Near-guaranteed restructuring
                    new_order = []
                    new_order.extend(random.sample(nouns, min(2, len(nouns))))
                    new_order.extend(random.sample(verbs, min(1, len(verbs))))
                    remaining = [w for w, p in pos_tags if not (p.startswith('NN') or p.startswith('VB'))]
                    random.shuffle(remaining)
                    new_order.extend(remaining)
                    sentence = " ".join(new_order)
                    changes.extend([w for w in words if w not in new_order or words.index(w) != new_order.index(w)])

            # Add connector for variation
            if random.random() < 0.8:
                connector = random.choice(self.connectors)
                sentence = f"{connector}, {sentence.lower()}"
                changes.append(connector)

            # Adjust tone with professional rephrasing
            if tone == "formal" and random.random() < 0.9:
                if "is" in sentence:
                    sentence = sentence.replace("is", "appears to be", 1)
                    changes.append("is → appears to be")
                elif "will" in sentence:
                    sentence = sentence.replace("will", "may", 1)
                    changes.append("will → may")

            # Capitalize first letter and ensure ending punctuation
            sentence = sentence[0].upper() + sentence[1:]
            if not sentence.endswith(('.', '?', '!')):
                sentence += '.'
                changes.append('.')

            return sentence, changes if sentence != original else []
        except Exception as e:
            print(f"Error paraphrasing sentence '{sentence}': {e}")
            return sentence, []

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
                    humanized, changes = self.paraphrase_sentence(sentence, tone)
                    humanized_sentences.append(humanized)
                    all_changes.extend(changes)
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