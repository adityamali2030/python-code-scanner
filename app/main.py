from app.documentation import generate_documentation
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.analyzer import analyze_code, MAX_CODE_LENGTH

app = FastAPI(
    title="Python Code Scanner",
    description="Analyze Python code structure without executing it.",
    version="0.1.0",
)


class AnalyzeRequest(BaseModel):
    code: str = Field(
        min_length=1,
        max_length=MAX_CODE_LENGTH,
        description="Python source code to analyze.",
    )


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze")
def analyze(request: AnalyzeRequest):
    try:
        return analyze_code(request.code)
    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail=str(error),
        ) from error
    except (RecursionError, MemoryError) as error:
        raise HTTPException(
            status_code=422,
            detail="Code is too complex to analyze.",
        ) from error

@app.post("/document")
def document(request: AnalyzeRequest):
    try:
        return {
            "markdown": generate_documentation(request.code)
        }
    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail=str(error),
        ) from error
    except (RecursionError, MemoryError) as error:
        raise HTTPException(
            status_code=422,
            detail="Code is too complex to analyze.",
        ) from error    