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


class AnalyzeRequest(BaseModel):
    prompt_id: Optional[int] = None
    content:   Optional[str] = None
    # El frontend puede mandar proveedor y modelo explicitamente
    provider:  Optional[str] = None
    model:     Optional[str] = None


class QuickAnalyzeRequest(BaseModel):
    content:  str
    provider: Optional[str] = None
    model:    Optional[str] = None


class ApiKeyConfig(BaseModel):
    provider: str   # "anthropic" | "openai" | "deepseek"
    api_key:  str


# ── Helpers para leer las keys del entorno ───────────────
ENV_KEYS = {
    "anthropic": "ANTHROPIC_API_KEY",
    "openai":    "OPENAI_API_KEY",
    "deepseek":  "DEEPSEEK_API_KEY",
}

def _get_active_key(provider: Optional[str] = None):
    """Devuelve (provider, key) activos. Si no se pasa provider, prueba los tres."""
    if provider:
        key = os.environ.get(ENV_KEYS.get(provider, ""), "")
        return (provider, key) if key else (provider, "")

    for prov, env_var in ENV_KEYS.items():
        key = os.environ.get(env_var, "")
        if key:
            return (prov, key)
    return (None, "")


# ── Endpoints ────────────────────────────────────────────
@router.post("/analyze", response_model=AnalysisOut)
async def analyze(req: AnalyzeRequest, db: Session = Depends(get_db)):
    provider, api_key = _get_active_key(req.provider)

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
        api_key=api_key,
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
    """Analisis rapido sin guardar en BD."""
    provider, api_key = _get_active_key(req.provider)
    result = await analyze_prompt(req.content, api_key=api_key, provider=provider, model=req.model)
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


# ── Configuracion de API keys ─────────────────────────────
@router.post("/config/api-key")
async def set_api_key(data: ApiKeyConfig):
    """Guarda o elimina una API key en variables de entorno de sesion."""
    provider = data.provider.lower()
    if provider not in ENV_KEYS:
        raise HTTPException(status_code=400, detail=f"Proveedor desconocido: {provider}")

    env_var = ENV_KEYS[provider]
    if data.api_key.strip():
        os.environ[env_var] = data.api_key.strip()
        return {"ok": True, "message": f"API key de {provider} configurada"}
    else:
        os.environ.pop(env_var, None)
        return {"ok": True, "message": f"API key de {provider} eliminada"}


@router.get("/config/providers")
async def get_providers_status():
    """Devuelve el estado de los tres proveedores y sus modelos disponibles."""
    providers = {}
    for prov, env_var in ENV_KEYS.items():
        key = os.environ.get(env_var, "")
        providers[prov] = {
            "configured": bool(key),
            "preview": f"{key[:12]}..." if len(key) > 12 else "",
            "models": PROVIDER_MODELS.get(prov, []),
            "default_model": DEFAULT_MODELS.get(prov, ""),
        }
    return providers
