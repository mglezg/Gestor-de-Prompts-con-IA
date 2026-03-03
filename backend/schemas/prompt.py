from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Any

class PromptBase(BaseModel):
    title: str
    content: str
    description: Optional[str] = ""
    project_id: Optional[int] = None
    tags: Optional[List[str]] = []
    model_target: Optional[str] = "general"

class PromptCreate(PromptBase):
    change_note: Optional[str] = "Versión inicial"

class PromptUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    description: Optional[str] = None
    project_id: Optional[int] = None
    tags: Optional[List[str]] = None
    model_target: Optional[str] = None
    change_note: Optional[str] = "Actualización"

class PromptVersionOut(BaseModel):
    id: int
    version_number: int
    title: str
    content: str
    change_note: str
    created_at: datetime

    class Config:
        from_attributes = True

class PromptOut(PromptBase):
    id: int
    current_version: int
    created_at: datetime
    updated_at: datetime
    versions: List[PromptVersionOut] = []

    class Config:
        from_attributes = True

class AnalysisCriteria(BaseModel):
    clarity: float
    specificity: float
    structure: float
    format: float
    context: float
    examples: float

class SuggestionItem(BaseModel):
    criterion: str
    issue: str
    suggestion: str
    priority: str  # high, medium, low

class AnalysisOut(BaseModel):
    id: int
    prompt_id: int
    prompt_version: int
    overall_score: float
    criteria_scores: dict
    suggestions: List[Any]
    strengths: List[str]
    summary: str
    model_used: str
    created_at: datetime

    class Config:
        from_attributes = True

# Export/Import schemas
class PromptExport(BaseModel):
    format_version: str = "1.0"
    app: str = "PromptManager"
    prompts: List[dict]

class PromptImport(BaseModel):
    format_version: Optional[str] = "1.0"
    app: Optional[str] = "PromptManager"
    prompts: List[dict]
