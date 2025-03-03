import random
import re

class AdvancedHumanizer:
    def __init__(self):
        # Expanded vocabulary for academic rewriting
        self.vocab = {
            "nouns": {
                "study": ["research", "investigation", "analysis", "examination", "inquiry"],
                "time": ["duration", "chronology", "interval", "period", "timing"],
                "motion": ["movement", "kinetics", "dynamics", "mobility", "activity"],
                "management": ["administration", "governance", "oversight", "direction", "control"],
                "productivity": ["efficiency", "output", "performance", "effectiveness", "yield"],
                "tasks": ["activities", "duties", "operations", "assignments", "functions"],
                "ways": ["methods", "techniques", "approaches", "processes", "strategies"],
                "field": ["discipline", "domain", "area", "sphere", "realm"],
                "contributors": ["innovators", "pioneers", "practitioners", "leaders", "figures"],
                "efficiency": ["effectiveness", "optimality", "productivity", "streamlining", "performance"],
                "movements": ["actions", "motions", "gestures", "activities", "operations"],
                "development": ["evolution", "progress", "advancement", "refinement", "growth"],
                "studies": ["investigations", "analyses", "researches", "examinations", "inquiries"]
            },
            "verbs": {
                "pioneered": ["initiated", "spearheaded", "originated", "introduced", "launched"],
                "known": ["recognized", "acknowledged", "noted", "celebrated", "famed"],
                "focused": ["concentrated", "emphasized", "prioritized", "directed", "centered"],
                "improve": ["enhance", "boost", "elevate", "refine", "optimize"],
                "analyzing": ["examining", "assessing", "evaluating", "investigating", "reviewing"],
                "determining": ["identifying", "establishing", "specifying", "defining", "ascertaining"],
                "perform": ["execute", "conduct", "undertake", "accomplish", "carry out"],
                "sought": ["aimed", "pursued", "endeavored", "strived", "intended"],
                "eliminate": ["remove", "eradicate", "exclude", "reduce", "abolish"],
                "increase": ["boost", "elevate", "enhance", "amplify", "augment"],
                "emphasized": ["highlighted", "stressed", "prioritized", "accentuated", "underlined"],
                "making": ["rendering", "shaping", "forming", "establishing", "constituting"],
                "was": ["existed as", "functioned as", "served as", "operated as", "acted as"],
                "is": ["stands as", "remains", "serves as", "functions as", "represents"]
            },
            "adjectives": {
                "common": ["shared", "mutual", "typical", "similar", "standard"],
                "distinct": ["unique", "specific", "separate", "individual", "particular"],
                "efficient": ["effective", "optimal", "productive", "streamlined", "practical"],
                "significant": ["notable", "important", "substantial", "key", "prominent"],
                "unnecessary": ["redundant", "excessive", "superfluous", "unneeded", "extraneous"],
                "complementary": ["synergistic", "supportive", "enhancing", "cooperative", "auxiliary"],
                "scientific": ["methodical", "systematic", "analytical", "rigorous", "technical"],
                "most": ["optimal", "prime", "leading", "top", "foremost"]
            },
            "prepositions": {
                "by": ["through", "via", "using", "with", "per"],
                "on": ["upon", "in", "through", "via", "with"],
                "to": ["toward", "for", "in", "at", "regarding"],
                "in": ["within", "across", "among", "throughout", "inside"]
            },
            "connectors": ["In essence", "Notably", "For instance", "In particular", "Conversely", "Moreover", "Thus"]
        }
        # Flexible sentence templates
        self.templates = [
            lambda conn, subj, verb, obj, mod: f"{conn}, {subj} {verb} {obj} {mod}",
            lambda conn, subj, verb, obj, mod: f"{conn}, the endeavor of {verb} {obj} by {subj} is shaped {mod}",
            lambda conn, subj, verb, obj, mod: f"{conn}, {verb} {obj} forms a cornerstone of {subj}’s efforts {mod}",
            lambda conn, subj, verb, obj, mod: f"{conn}, through {verb} {obj}, {subj} advances {mod}",
            lambda conn, subj, verb, obj, mod: f"{conn}, {subj}’s focus {mod} underpins the {verb} of {obj}"
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

    def paraphrase_sentence(self, sentence):
        try:
            original = sentence.strip()
            if not original:
                return original, []
            words = original.split()
            changes = []

            # Extract entities and key components
            entities = []
            for entity in ["Frederick Winslow Taylor", "Frank and Lillian Gilbreth", "Taylor", "Gilbreths"]:
                if entity in original:
                    entities.append(entity)
            if not entities:
                entities = ["research efforts"]  # Fallback subject

            # Identify verb, object, and modifiers
            verb_candidates = [w for w in words if w.lower() in self.vocab["verbs"]]
            verb = verb_candidates[0] if verb_candidates else "explored"
            obj_candidates = [w for w in words if w.lower() in self.vocab["nouns"] and w not in entities]
            obj = obj_candidates[0] if obj_candidates else "concepts"
            modifiers = " ".join([w for w in words if w not in entities and w != verb and w != obj])

            # Replace with synonyms
            new_entities = []
            for entity in entities:
                if entity in ["Frederick Winslow Taylor", "Frank and Lillian Gilbreth"]:
                    new_entities.append(entity)  # Preserve full names
                else:
                    new_entity, ent_changes = self.get_synonym(entity, "nouns")
                    new_entities.append(new_entity)
                    changes.extend(ent_changes)
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
            changes.extend(verb_changes + obj_changes)

            # Apply template with entity as subject
            subject = ", ".join(new_entities)
            template = random.choice(self.templates)
            sentence = template(random.choice(self.vocab["connectors"]), subject, new_verb, new_obj, new_modifiers)
            changes.extend([w for w in original.split() if w not in sentence.split()])

            # Capitalize and punctuate
            sentence = sentence[0].upper() + sentence[1:]
            if not sentence.endswith(('.', '?', '!')):
                sentence += '.'

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
            return final_text
        except Exception as e:
            print(f"Critical error in humanization: {e}")
            return f"Cannot humanize: {str(e)}. Original text: {ai_text}", []