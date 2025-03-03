import random
import re

class AdvancedHumanizer:
    def __init__(self):
        # Comprehensive vocabulary for academic/business rewriting
        self.vocab = {
            "nouns": {
                "market": ["marketplace", "sector", "industry", "domain", "arena"],
                "groups": ["categories", "clusters", "segments", "divisions", "classes"],
                "characteristics": ["attributes", "traits", "features", "qualities", "properties"],
                "strategy": ["approach", "method", "framework", "tactic", "plan"],
                "segments": ["sectors", "portions", "areas", "parts", "divisions"],
                "image": ["identity", "reputation", "profile", "impression", "persona"],
                "mind": ["perception", "awareness", "consciousness", "perspective", "view"],
                "consumer": ["customer", "client", "buyer", "user", "individual"],
                "tool": ["instrument", "resource", "mechanism", "apparatus", "method"],
                "perceptions": ["views", "impressions", "insights", "judgments", "opinions"],
                "brands": ["entities", "products", "offerings", "labels", "marks"],
                "competitors": ["rivals", "peers", "adversaries", "contenders", "opponents"],
            },
            "verbs": {
                "Designing": ["Crafting", "Formulating", "Devising", "Shaping", "Developing"],
                "Dividing": ["Segmenting", "Partitioning", "Separating", "Categorizing", "Distributing"],
                "Selecting": ["Identifying", "Choosing", "Determining", "Picking", "Targeting"],
                "Establishing": ["Creating", "Defining", "Building", "Forming", "Instituting"],
                "visualize": ["illustrate", "depict", "represent", "portray", "demonstrate"],
                "serve": ["address", "support", "cater to", "assist", "engage"],
                "used": ["employed", "utilized", "applied", "leveraged", "implemented"],
                "ranging": ["spanning", "extending", "covering", "varying", "encompassing"],
            },
            "adjectives": {
                "common": ["shared", "mutual", "typical", "similar", "standard"],
                "distinct": ["unique", "specific", "separate", "individual", "particular"],
                "attractive": ["appealing", "desirable", "compelling", "engaging", "noteworthy"],
                "specific": ["precise", "targeted", "focused", "defined", "exact"],
            },
            "prepositions": {
                "based on": ["grounded in", "derived from", "built upon", "informed by", "stemming from"],
                "into": ["within", "across", "among", "throughout", "inside"],
                "relative to": ["compared with", "in relation to", "versus", "against", "concerning"],
                "on": ["upon", "in", "through", "via", "with"],
            },
            "connectors": ["In essence", "Notably", "For instance", "In particular", "Conversely", "Specifically", "On the other hand"]
        }
        # Sentence structure templates for full rewrite
        self.templates = [
            lambda subj, verb, obj, mod: f"{verb} {obj}, {subj} reflects a focus on {mod}",
            lambda subj, verb, obj, mod: f"{subj} employs {verb} to shape {obj} through {mod}",
            lambda subj, verb, obj, mod: f"The process of {verb} {obj} by {subj} hinges on {mod}",
            lambda subj, verb, obj, mod: f"{subj}, via {verb}, constructs {obj} with attention to {mod}",
            lambda subj, verb, obj, mod: f"{verb} {obj} represents {subj}’s approach to {mod}"
        ]

    def get_synonym(self, word, category="nouns"):
        word_lower = word.lower()
        if word_lower in self.vocab[category]:
            choice = random.choice(self.vocab[category][word_lower])
            return choice, [word] if choice.lower() != word_lower else []
        return word, []

    def split_sentences(self, text):
        # Robust sentence splitting
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())
        return [s.strip() for s in sentences if s.strip()]

    def decompose_sentence(self, sentence):
        words = sentence.split()
        subject = next((word for word in words if word.lower() in self.vocab["nouns"]), "This")
        verb = next((word for word in words if word.lower() in self.vocab["verbs"]), "involves")
        obj = next((word for word in words if word.lower() in self.vocab["nouns"] and word != subject), "process")
        modifiers = " ".join([w for w in words if w not in (subject, verb, obj) and w not in self.vocab["connectors"]])
        return subject, verb, obj, modifiers if modifiers else "various elements"

    def paraphrase_sentence(self, sentence):
        try:
            original = sentence.strip()
            if not original:
                return original, []
            changes = []

            # Decompose sentence
            subject, verb, obj, modifiers = self.decompose_sentence(original)

            # Replace with synonyms
            new_subject, subj_changes = self.get_synonym(subject, "nouns")
            new_verb, verb_changes = self.get_synonym(verb, "verbs")
            new_obj, obj_changes = self.get_synonym(obj, "nouns")
            modifier_words = modifiers.split()
            new_modifiers = []
            for mod in modifier_words:
                if mod.lower() in self.vocab["adjectives"]:
                    new_mod, mod_changes = self.get_synonym(mod, "adjectives")
                elif mod.lower() in self.vocab["prepositions"]:
                    new_mod, mod_changes = self.get_synonym(mod, "prepositions")
                else:
                    new_mod, mod_changes = mod, []
                new_modifiers.append(new_mod)
                changes.extend(mod_changes)
            new_modifiers = " ".join(new_modifiers)
            changes.extend(subj_changes + verb_changes + obj_changes)

            # Apply random structure template
            template = random.choice(self.templates)
            sentence = template(new_subject, new_verb, new_obj, new_modifiers)
            changes.extend([w for w in original.split() if w not in sentence.split()])

            # Add connector
            connector = random.choice(self.vocab["connectors"])
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