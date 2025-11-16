import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from fastapi import FastAPI, Body, HTTPException
from pydantic import BaseModel
from services.setup_workflow import setup_workflow

app = FastAPI()


# Pydantic models for request and response bodies
class RecommendRequest(BaseModel):
    model_name: str
    user_input: str


class RecommendResponse(BaseModel):
    parsed_query: dict
    suggestions: list


workflow = None


def validate_prompt(prompt: str):
    if not prompt or not prompt.strip():
        raise HTTPException(
            status_code=400, detail="Bạn cần nhập yêu cầu về đồ ăn/thức uống!"
        )


# API endpoint for food/drink recommendation
@app.post("/recommend", response_model=RecommendResponse)
def recommend_food(req: RecommendRequest):
    validate_prompt(req.user_input)
    global workflow
    if workflow is None or getattr(workflow, "model_name", None) != req.model_name:
        workflow = setup_workflow(model_name_or_path=req.model_name)
        if workflow is None:
            raise HTTPException(status_code=500, detail="Workflow setup failed.")
    result = workflow.process_user_request(req.user_input)
    if result.get("status") != "success":
        raise HTTPException(
            status_code=500,
            detail=result.get("error", "Lỗi không xác định từ workflow."),
        )
    parsed_query = result["parsed_query"]
    suggestions = result.get("suggestions")
    if suggestions is None:
        suggestions = []
    return RecommendResponse(parsed_query=parsed_query, suggestions=suggestions)


@app.post("/reset")
def reset_workflow():
    global workflow
    workflow = None
    return {"status": "reset", "message": "Workflow has been reset."}
