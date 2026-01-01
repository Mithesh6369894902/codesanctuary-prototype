import os
import difflib
from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np

class SemanticRecoveryEngine:
    def __init__(self, model_name="microsoft/codebert-base"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)

    def embed_code(self, code: str):
        inputs = self.tokenizer(code, return_tensors="pt", truncation=True, max_length=512)
        with torch.no_grad():
            emb = self.model(**inputs).last_hidden_state.mean(dim=1).squeeze()
        return emb.numpy()

    def semantic_similarity(self, code_a, code_b):
        emb_a = self.embed_code(code_a)
        emb_b = self.embed_code(code_b)
        sim = np.dot(emb_a, emb_b) / (np.linalg.norm(emb_a) * np.linalg.norm(emb_b))
        return float(sim)

    def suggest_recovery(self, broken_code, repo_path="data/sample_repo/"):
        best_file, best_score = None, -1
        for fname in os.listdir(repo_path):
            if fname.endswith(".py"):
                with open(os.path.join(repo_path, fname)) as f:
                    original = f.read()
                score = self.semantic_similarity(broken_code, original)
                if score > best_score:
                    best_file, best_score = fname, score
        return best_file, best_score
