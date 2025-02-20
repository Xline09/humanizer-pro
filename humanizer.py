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
            "Moreover": ["Also", "Besides", "Plus", "On top of that", "And", "What’s more"],
            "Additionally": ["Furthermore", "Also", "On top of that", "Plus", "Another thing", "On the other hand"],
            "Furthermore": ["Moreover", "Also", "Besides", "Plus", "And", "What’s more"],
            "However": ["But", "Yet", "Still", "Though", "Even so", "Nonetheless"],
            "Therefore": ["So", "Thus", "Hence", "As a result", "That’s why", "Because of that"]
        }
        self.human_phrases = {
            "casual": ["you know", "I think", "kinda", "sorta", "tbh", "just saying", "no kidding", "if you ask me"],
            "formal": ["in my view", "it appears that", "arguably", "it might be said", "one could argue"],
            "mixed": ["to be honest", "for what it’s worth", "believe it or not", "frankly"]
        }
        self.slang = {"you": ["u"], "are": ["r"], "going to": ["gonna"], "want to": ["wanna"], "have to": ["hafta"]}
        self.punctuation_variations = ['.', '!', '?', '...', '!?', '..', '!.']
        self.emoticons = [":)", ":(", ";)", ":D", ":P", "lol", "haha", "meh", ":/"]
        self.typos = {"the": ["teh", "hte"], "and": ["an", "nad"], "is": ["si", "is"], "to": ["ot", "to"]}
        self.stop_words = set(stopwords.words('english'))
        try:
            self.sentiment_analyzer = SentimentIntensityAnalyzer()
        except Exception as e:
            print(f"Failed to initialize SentimentIntensityAnalyzer: {e}")
            self.sentiment_analyzer = None

        self.personal_touches = [
            "last week I noticed something similar", "in my experience", "from what I’ve seen", "I remember reading that",
            "a friend mentioned this once", "it reminds me of something"
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
            return self.synonym_cache[word]
        except Exception as e:
            print(f"Error getting synonyms: {e}")
            return [word]

    def introduce_errors(self, sentence, tone):
        try:
            words = self._safe_tokenize(sentence)
            for i, word in enumerate(words):
                if tone != "formal" and word.lower() in self.typos and random.random() < 0.08:
                    words[i] = random.choice(self.typos[word.lower()])
                if tone != "formal" and word.lower() in self.slang and random.random() < 0.12:
                    words[i] = random.choice(self.slang[word.lower()])
            return " ".join(words)
        except Exception as e:
            print(f"Error introducing errors: {e}")
            return sentence

    def vary_sentence_length(self, sentence, tone):
        try:
            words = self._safe_tokenize(sentence)
            if len(words) > 12 and random.random() < 0.6:
                words = words[:random.randint(6, len(words) // 2)]
                if tone != "formal" and random.random() < 0.4:
                    words.append(random.choice(self.human_phrases.get(tone, self.human_phrases["mixed"])))
            elif len(words) < 6 and random.random() < 0.5:
                words.extend(random.choice(self.human_phrases.get(tone, self.human_phrases["mixed"])).split() + [random.choice([".", "!"])])
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
            if random.random() < 0.4:
                insert_pos = random.randint(0, len(sentence.split()))
                words = sentence.split()
                phrase_set = self.human_phrases.get(tone, self.human_phrases["mixed"])
                words.insert(insert_pos, random.choice(phrase_set))
                sentence = " ".join(words)
            if tone != "formal" and random.random() < 0.25:
                sentence += " " + random.choice(self.emoticons)
            if tone != "formal" and random.random() < 0.15:
                sentence += random.choice([" lol", " haha", " right?", " ya know"])
            if random.random() < 0.1:
                sentence = random.choice(self.personal_touches) + ", " + sentence
            return sentence
        except Exception as e:
            print(f"Error adding human touch: {e}")
            return sentence

    def restructure_sentence(self, sentence):
        try:
            words = self._safe_tokenize(sentence)
            if len(words) > 6 and random.random() < 0.5:
                try:
                    pos_tags = nltk.pos_tag(words)
                    nouns = [word for word, pos in pos_tags if pos.startswith('NN')]
                    verbs = [word for word, pos in pos_tags if pos.startswith('VB')]
                    if nouns and verbs:
                        new_order = []
                        order_type = random.choice(["noun_verb", "verb_noun"])
                        if order_type == "noun_verb":
                            new_order.extend(random.sample(nouns, min(2, len(nouns))))
                            new_order.extend(random.sample(verbs, min(1, len(verbs))))
                        else:
                            new_order.extend(random.sample(verbs, min(1, len(verbs))))
                            new_order.extend(random.sample(nouns, min(2, len(nouns))))
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
                if random.random() < 0.2:
                    sentence = re.sub(r'\bis\b', random.choice(["seems to be", "appears to be"]), sentence, 1)
                    sentence = re.sub(r'\bwill\b', random.choice(["might", "could"]), sentence, 1)
            elif original_tone == "casual":
                if random.random() < 0.3:
                    sentence += random.choice([" dude", " seriously"])
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
                    sentence = self.introduce_errors(sentence, tone)
                    sentence = self.adjust_tone(sentence, tone)
                    if random.random() < 0.25:
                        last_char = sentence[-1] if sentence else ''
                        if last_char in string.punctuation:
                            sentence = sentence.rstrip(last_char) + random.choice(self.punctuation_variations)
                    humanized_sentences.append(sentence)
                except Exception as e:
                    print(f"Error processing sentence '{sentence}': {e}")
                    humanized_sentences.append(sentence)
            final_text = " ".join(humanized_sentences).strip()
            if random.random() < 0.12:
                final_text += "\n\n" + random.choice(["Anyway,", "So yeah,", "That’s it,", "For now,"]) + " " + random.choice(self.emoticons if tone != "formal" else [""])
            if not final_text:
                return "Humanization resulted in no output. Original text returned."
            return final_text
        except Exception as e:
            print(f"Critical error in humanization: {e}")
            return f"Cannot humanize: {str(e)}. Original text: {ai_text}"