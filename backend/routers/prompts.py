from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
import json
from datetime import datetime
from backend.database import get_db
from backend.models.prompt import Prompt, PromptVersion
from backend.schemas.prompt import PromptCreate, PromptUpdate, PromptOut, PromptVersionOut

router = APIRouter(prefix="/prompts", tags=["prompts"])

def _save_version(db: Session, prompt: Prompt, change_note: str = ""):
    version = PromptVersion(
        prompt_id=prompt.id,
        version_number=prompt.current_version,
        content=prompt.content,
        title=prompt.title,
        change_note=change_note
    )
    db.add(version)

@router.get("/", response_model=List[PromptOut])
def list_prompts(
    project_id: Optional[int] = Query(None),
    search: Optional[str] = Query(None),
    tags: Optional[str] = Query(None),
    model_target: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    q = db.query(Prompt)
    if project_id is not None:
        q = q.filter(Prompt.project_id == project_id)
    if search:
        term = f"%{search}%"
        q = q.filter(or_(
            Prompt.title.ilike(term),
            Prompt.content.ilike(term),
            Prompt.description.ilike(term)
        ))
    if model_target:
        q = q.filter(Prompt.model_target == model_target)
    prompts = q.order_by(Prompt.updated_at.desc()).all()

    # Filter by tags in Python (JSON array stored as text)
    if tags:
        tag_list = [t.strip() for t in tags.split(",")]
        prompts = [p for p in prompts if any(t in (p.tags or []) for t in tag_list)]

    return prompts

@router.post("/", response_model=PromptOut, status_code=201)
def create_prompt(data: PromptCreate, db: Session = Depends(get_db)):
    change_note = data.change_note or "Versión inicial"
    prompt_data = data.model_dump(exclude={"change_note"})
    prompt = Prompt(**prompt_data)
    prompt.current_version = 1
    db.add(prompt)
    db.flush()
    _save_version(db, prompt, change_note)
    db.commit()
    db.refresh(prompt)
    return prompt

@router.get("/{prompt_id}", response_model=PromptOut)
def get_prompt(prompt_id: int, db: Session = Depends(get_db)):
    prompt = db.query(Prompt).filter(Prompt.id == prompt_id).first()
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt no encontrado")
    return prompt

@router.put("/{prompt_id}", response_model=PromptOut)
def update_prompt(prompt_id: int, data: PromptUpdate, db: Session = Depends(get_db)):
    prompt = db.query(Prompt).filter(Prompt.id == prompt_id).first()
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt no encontrado")

    change_note = data.change_note or "Actualización"
    update_data = data.model_dump(exclude_none=True, exclude={"change_note"})

    # Bump version only if content changed
    content_changed = "content" in update_data and update_data["content"] != prompt.content
    if content_changed:
        prompt.current_version += 1

    for field, value in update_data.items():
        setattr(prompt, field, value)

    if content_changed:
        _save_version(db, prompt, change_note)

    prompt.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(prompt)
    return prompt

@router.delete("/{prompt_id}")
def delete_prompt(prompt_id: int, db: Session = Depends(get_db)):
    prompt = db.query(Prompt).filter(Prompt.id == prompt_id).first()
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt no encontrado")
    db.delete(prompt)
    db.commit()
    return {"ok": True, "message": "Prompt eliminado"}

@router.get("/{prompt_id}/versions", response_model=List[PromptVersionOut])
def get_versions(prompt_id: int, db: Session = Depends(get_db)):
    prompt = db.query(Prompt).filter(Prompt.id == prompt_id).first()
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt no encontrado")
    return prompt.versions

@router.post("/{prompt_id}/restore/{version_number}", response_model=PromptOut)
def restore_version(prompt_id: int, version_number: int, db: Session = Depends(get_db)):
    prompt = db.query(Prompt).filter(Prompt.id == prompt_id).first()
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt no encontrado")
    version = db.query(PromptVersion).filter(
        PromptVersion.prompt_id == prompt_id,
        PromptVersion.version_number == version_number
    ).first()
    if not version:
        raise HTTPException(status_code=404, detail="Versión no encontrada")

    prompt.current_version += 1
    prompt.content = version.content
    prompt.title = version.title
    prompt.updated_at = datetime.utcnow()
    _save_version(db, prompt, f"Restaurado desde v{version_number}")
    db.commit()
    db.refresh(prompt)
    return prompt

# Export
@router.get("/export/json")
def export_prompts(
    project_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    q = db.query(Prompt)
    if project_id:
        q = q.filter(Prompt.project_id == project_id)
    prompts = q.all()

    export_data = {
        "format_version": "1.0",
        "app": "PromptManager",
        "exported_at": datetime.utcnow().isoformat(),
        "prompts": [
            {
                "title": p.title,
                "content": p.content,
                "description": p.description,
                "tags": p.tags or [],
                "model_target": p.model_target,
                "version": p.current_version,
                "created_at": p.created_at.isoformat()
            }
            for p in prompts
        ]
    }
    return JSONResponse(content=export_data)

# Import
@router.post("/import/json")
async def import_prompts(data: dict, db: Session = Depends(get_db)):
    if data.get("app") != "PromptManager":
        raise HTTPException(status_code=400, detail="Formato de archivo no reconocido")

    imported = 0
    for p in data.get("prompts", []):
        prompt = Prompt(
            title=p.get("title", "Prompt importado"),
            content=p.get("content", ""),
            description=p.get("description", ""),
            tags=p.get("tags", []),
            model_target=p.get("model_target", "general"),
            current_version=1
        )
        db.add(prompt)
        db.flush()
        _save_version(db, prompt, "Importado desde archivo")
        imported += 1

    db.commit()
    return {"ok": True, "imported": imported}

# Get all unique tags
@router.get("/meta/tags")
def get_all_tags(db: Session = Depends(get_db)):
    prompts = db.query(Prompt.tags).all()
    tags = set()
    for (tag_list,) in prompts:
        if tag_list:
            tags.update(tag_list)
    return sorted(list(tags))
