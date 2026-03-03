from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import os
from backend.database import get_db
from backend.models.prompt import Prompt
from backend.models.analysis import Analysis
from backend.schemas.prompt import AnalysisOut
from backend.services.prompt_analyzer import analyze_prompt
from backend.services.prompt_criteria import CRITERIA, MODEL_TARGETS
from pydantic import BaseModel

router = APIRouter(prefix="/analysis", tags=["analysis"])

class AnalyzeRequest(BaseModel):
    prompt_id: Optional[int] = None
    content: Optional[str] = None
    api_key: Optional[str] = None

class QuickAnalyzeRequest(BaseModel):
    content: str
    api_key: Optional[str] = None

@router.post("/analyze", response_model=AnalysisOut)
async def analyze(req: AnalyzeRequest, db: Session = Depends(get_db)):
    # Get API key from env or request
    api_key = req.api_key or os.environ.get("ANTHROPIC_API_KEY")

    if req.prompt_id:
        prompt = db.query(Prompt).filter(Prompt.id == req.prompt_id).first()
        if not prompt:
            raise HTTPException(status_code=404, detail="Prompt no encontrado")
        content = prompt.content
        version = prompt.current_version
    elif req.content:
        content = req.content
        version = 0
    else:
        raise HTTPException(status_code=400, detail="Se requiere prompt_id o content")

    result = await analyze_prompt(content, api_key)

    analysis = Analysis(
        prompt_id=req.prompt_id or 0,
        prompt_version=version,
        overall_score=result["overall_score"],
        criteria_scores=result["criteria_scores"],
        suggestions=result["suggestions"],
        strengths=result.get("strengths", []),
        summary=result.get("summary", ""),
        model_used=result.get("model_used", "heuristic")
    )

    if req.prompt_id:
        db.add(analysis)
        db.commit()
        db.refresh(analysis)
    else:
        # For quick analysis (no prompt_id), return without saving
        from datetime import datetime
        analysis.id = 0
        analysis.created_at = datetime.utcnow()

    return analysis

@router.post("/quick")
async def quick_analyze(req: QuickAnalyzeRequest):
    """Análisis rápido sin guardar en BD."""
    api_key = req.api_key or os.environ.get("ANTHROPIC_API_KEY")
    result = await analyze_prompt(req.content, api_key)
    return result

@router.get("/prompt/{prompt_id}", response_model=List[AnalysisOut])
def get_prompt_analyses(prompt_id: int, db: Session = Depends(get_db)):
    return db.query(Analysis).filter(
        Analysis.prompt_id == prompt_id
    ).order_by(Analysis.created_at.desc()).all()

@router.get("/criteria")
def get_criteria():
    return CRITERIA

@router.get("/model-targets")
def get_model_targets():
    return MODEL_TARGETS

@router.post("/config/api-key")
async def set_api_key(data: dict):
    """Guarda la API key en variable de entorno de sesión."""
    key = data.get("api_key", "")
    if key:
        os.environ["ANTHROPIC_API_KEY"] = key
        return {"ok": True, "message": "API key configurada correctamente"}
    else:
        os.environ.pop("ANTHROPIC_API_KEY", None)
        return {"ok": True, "message": "API key eliminada"}

@router.get("/config/api-key-status")
async def api_key_status():
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    return {
        "configured": bool(key and key.startswith("sk-ant-")),
        "preview": f"{key[:10]}..." if len(key) > 10 else ""
    }
