import random
import re
from transformers import AutoTokenizer, AutoModel
import torch
import os
import numpy as np

class AdvancedHumanizer:
    def __init__(self):
        # Load pre-downloaded model and tokenizer
        model_dir = os.path.join(os.path.dirname(__file__), "paraphrase-MiniLM-L6-v2")
        if not os.path.exists(model_dir):
            raise ValueError(f"Model directory {model_dir} not found. Ensure 'paraphrase-MiniLM-L6-v2' is included.")
        self.tokenizer = AutoTokenizer.from_pretrained(model_dir)
        self.model = AutoModel.from_pretrained(model_dir)
        self.device = torch.device("cpu")
        self.model.to(self.device)

        # Academic vocabulary for reconstruction
        self.polish_vocab = {
            "nouns": {
                "study": ["investigation", "research", "analysis", "inquiry"],
                "time": ["duration", "interval", "period", "chronology"],
                "motion": ["movement", "kinetics", "dynamics", "activity"],
                "management": ["administration", "governance", "oversight"],
                "productivity": ["efficiency", "output", "effectiveness"],
                "tasks": ["duties", "operations", "assignments"],
                "ways": ["methods", "techniques", "approaches"],
                "field": ["discipline", "domain", "sphere"],
                "contributors": ["innovators", "practitioners", "pioneers"],
                "efficiency": ["effectiveness", "optimality", "performance"],
                "movements": ["actions", "operations", "activities"],
                "development": ["evolution", "progress", "advancement"],
                "studies": ["analyses", "researches", "examinations"],
                "market": ["marketplace", "sector", "industry"],
                "groups": ["categories", "clusters", "segments"],
                "strategy": ["approach", "framework", "plan"],
                "image": ["identity", "reputation", "profile"]
            },
            "verbs": {
                "pioneered": ["initiated", "spearheaded", "originated"],
                "known": ["recognized", "noted", "acknowledged"],
                "focused": ["concentrated", "emphasized", "prioritized"],
                "improve": ["enhance", "boost", "refine"],
                "analyzing": ["examining", "assessing", "evaluating"],
                "determining": ["identifying", "specifying", "defining"],
                "perform": ["execute", "conduct", "undertake"],
                "sought": ["aimed", "pursued", "endeavored"],
                "eliminate": ["remove", "exclude", "reduce"],
                "increase": ["boost", "elevate", "enhance"],
                "emphasized": ["highlighted", "stressed", "accentuated"],
                "making": ["rendering", "forming", "shaping"],
                "was": ["served as", "functioned as", "acted as"],
                "is": ["stands as", "remains", "represents"],
                "dividing": ["segmenting", "partitioning", "separating"],
                "selecting": ["choosing", "targeting", "picking"],
                "establishing": ["defining", "creating", "forming"]
            },
            "connectors": ["In essence", "Notably", "For instance", "In particular", "Conversely", "Moreover", "Thus"]
        }
        self.templates = [
            "{conn}, {subj} {verb} {obj} {mod}",
            "{conn}, the {obj} {verb} by {subj} advances {mod}",
            "{conn}, through {verb} {obj}, {subj} leverages {mod}",
            "{conn}, {subj}’s {verb} of {obj} reflects {mod}"
        ]

    def split_sentences(self, text):
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())
        return [s.strip() for s in sentences if s.strip()]

    def get_embeddings(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512).to(self.device)
        with torch.no_grad():
            outputs = self.model(**inputs)
        return outputs.last_hidden_state.mean(dim=1).cpu().numpy()

    def paraphrase(self, text):
        # Simple paraphrasing: extract key terms, reconstruct with template
        words = text.split()
        subj = next((w for w in words if w.lower() in self.polish_vocab["nouns"] or w in ["Frederick", "Frank", "Lillian", "Taylor", "Gilbreths"]), "research")
        verb = next((w for w in words if w.lower() in self.polish_vocab["verbs"]), "explored")
        obj = next((w for w in words if w.lower() in self.polish_vocab["nouns"] and w != subj), "concepts")
        mod = " ".join([w for w in words if w not in [subj, verb, obj] and w not in self.polish_vocab["connectors"]])

        new_subj = subj if subj in ["Frederick", "Frank", "Lillian", "Taylor", "Gilbreths"] else self.get_synonym(subj.lower(), "nouns")[0]
        new_verb = self.get_synonym(verb.lower(), "verbs")[0]
        new_obj = self.get_synonym(obj.lower(), "nouns")[0]
        new_mod = self.polish_text(mod)

        template = random.choice(self.templates)
        return template.format(conn="{conn}", subj=new_subj, verb=new_verb, obj=new_obj, mod=new_mod)

    def polish_text(self, text):
        words = text.split()
        polished_words = []
        for word in words:
            word_lower = word.lower()
            for category in ["nouns", "verbs"]:
                if word_lower in self.polish_vocab[category]:
                    new_word, _ = self.get_synonym(word_lower, category)
                    polished_words.append(new_word)
                    break
            else:
                polished_words.append(word)
        return " ".join(polished_words)

    def get_synonym(self, word, category):
        if word in self.polish_vocab[category]:
            choice = random.choice(self.polish_vocab[category][word])
            return choice, [word] if choice != word else []
        return word, []

    def humanize(self, ai_text):
        try:
            if not ai_text.strip():
                return "No text provided to humanize."
            sentences = self.split_sentences(ai_text)
            humanized_sentences = []

            for sentence in sentences:
                if not sentence:
                    continue
                paraphrased = self.paraphrase(sentence)
                connector = random.choice(self.polish_vocab["connectors"])
                humanized = f"{connector}, {paraphrased[0].lower() + paraphrased[1:]}"
                humanized = humanized[0].upper() + humanized[1:]
                if not humanized.endswith(('.', '?', '!')):
                    humanized += '.'
                humanized_sentences.append(humanized)

            final_text = " ".join(humanized_sentences).strip()
            if not final_text:
                return "Humanization resulted in no output. Original text returned."
            return final_text
        except Exception as e:
            print(f"Error in humanization: {e}")
            return f"Cannot humanize: {str(e)}. Original text: {ai_text}"