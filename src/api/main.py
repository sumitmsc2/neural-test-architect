from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from typing import List, Optional
from src.generator.engine import TestGenerator, SelfHealingEngine

app = FastAPI(
    title="Neural Test Architect API",
    description="Enterprise-grade AI Quality Assurance API",
    version="1.0.0"
)

# Initialize engines
generator = TestGenerator()
healer = SelfHealingEngine()

class FeatureRequest(BaseModel):
    feature_description: str
    context: Optional[str] = "Web Application"

class TestResponse(BaseModel):
    id: str
    title: str
    steps: List[str]
    automation_script: str
    ai_confidence: float

class HealRequest(BaseModel):
    broken_script: str
    error_log: str

@app.get("/")
async def root():
    return {"status": "ok", "message": "Neural Test Architect Online"}

@app.post("/generate", response_model=TestResponse)
async def generate_test(request: FeatureRequest):
    """
    Generate test cases and scripts from feature descriptions.
    """
    try:
        result = generator.generate_test_case(request.feature_description)
        return TestResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/heal")
async def heal_test_script(request: HealRequest):
    """
    Auto-repair broken test scripts based on failure logs.
    """
    try:
        healed = healer.heal_script(request.broken_script, request.error_log)
        return {"original_script": request.broken_script, "healed_script": healed, "status": "healed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)