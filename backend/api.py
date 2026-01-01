from fastapi import FastAPI
from pydantic import BaseModel
from backend.recovery_engine import SemanticRecoveryEngine

app = FastAPI()
engine = SemanticRecoveryEngine()

class CodeInput(BaseModel):
    broken_code: str

@app.post("/recover/")
def recover_code(data: CodeInput):
    file, score = engine.suggest_recovery(data.broken_code)
    return {"suggested_file": file, "similarity_score": score}
