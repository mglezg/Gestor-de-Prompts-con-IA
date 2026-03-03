from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import os
from datetime import datetime
from backend.database import get_db
from backend.models.prompt import Prompt
from backend.models.analysis import Analysis
from backend.schemas.prompt import AnalysisOut
from backend.services.prompt_analyzer import analyze_prompt, PROVIDER_MODELS, DEFAULT_MODELS
from backend.services.prompt_criteria import CRITERIA, MODEL_TARGETS
from pydantic import BaseModel

router = APIRouter(prefix="/analysis", tags=["analysis"])

# ── Almacen de API keys en memoria del proceso ────────────
# Se usa un dict en el modulo para que persista entre requests
# dentro del mismo proceso worker (no se pierde como os.environ
# entre procesos padre/hijo de uvicorn --reload)
_api_keys: dict = {
    "anthropic": os.environ.get("ANTHROPIC_API_KEY", ""),
    "openai":    os.environ.get("OPENAI_API_KEY", ""),
    "deepseek":  os.environ.get("DEEPSEEK_API_KEY", ""),
}


class AnalyzeRequest(BaseModel):
    model_config = {"protected_namespaces": ()}
    prompt_id: Optional[int] = None
    content:   Optional[str] = None
    provider:  Optional[str] = None
    model:     Optional[str] = None


class QuickAnalyzeRequest(BaseModel):
    content:  str
    provider: Optional[str] = None
    model:    Optional[str] = None


class ApiKeyConfig(BaseModel):
    provider: str
    api_key:  str


def _resolve_provider_and_key(requested_provider: Optional[str]):
    """
    Devuelve (provider, key) segun el proveedor solicitado.
    Si es None o 'auto', usa el primer proveedor con key configurada.
    """
    if requested_provider and requested_provider != "auto":
        key = _api_keys.get(requested_provider, "")
        return (requested_provider, key)

    # Modo auto: primer proveedor con key
    for prov in ("anthropic", "openai", "deepseek"):
        key = _api_keys.get(prov, "")
        if key:
            return (prov, key)

    return (None, "")


# ── Endpoints ────────────────────────────────────────────
@router.post("/analyze", response_model=AnalysisOut)
async def analyze(req: AnalyzeRequest, db: Session = Depends(get_db)):
    provider, api_key = _resolve_provider_and_key(req.provider)

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

    result = await analyze_prompt(
        content,
        api_key=api_key or "",
        provider=provider,
        model=req.model
    )

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
        analysis.id = 0
        analysis.created_at = datetime.utcnow()

    return analysis


@router.post("/quick")
async def quick_analyze(req: QuickAnalyzeRequest):
    provider, api_key = _resolve_provider_and_key(req.provider)
    result = await analyze_prompt(req.content, api_key=api_key or "", provider=provider, model=req.model)
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
async def set_api_key(data: ApiKeyConfig):
    """Guarda la API key en el diccionario en memoria del proceso."""
    provider = data.provider.lower()
    if provider not in _api_keys:
        raise HTTPException(status_code=400, detail=f"Proveedor desconocido: {provider}")

    _api_keys[provider] = data.api_key.strip()
    if data.api_key.strip():
        return {"ok": True, "message": f"API key de {provider} configurada"}
    else:
        return {"ok": True, "message": f"API key de {provider} eliminada"}


@router.get("/config/providers")
async def get_providers_status():
    """Estado de los tres proveedores y sus modelos disponibles."""
    result = {}
    for prov in ("anthropic", "openai", "deepseek"):
        key = _api_keys.get(prov, "")
        result[prov] = {
            "configured": bool(key),
            "preview": f"{key[:12]}..." if len(key) > 12 else "",
            "models": PROVIDER_MODELS.get(prov, []),
            "default_model": DEFAULT_MODELS.get(prov, ""),
        }
    return result
