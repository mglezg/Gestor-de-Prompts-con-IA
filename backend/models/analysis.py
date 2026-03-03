from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base

class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    prompt_id = Column(Integer, ForeignKey("prompts.id", ondelete="CASCADE"), nullable=False)
    prompt_version = Column(Integer, nullable=False)
    overall_score = Column(Float, nullable=False)
    criteria_scores = Column(JSON, nullable=False)  # {clarity, specificity, structure, format, context, examples}
    suggestions = Column(JSON, nullable=False)       # [{criterion, issue, suggestion, priority}]
    strengths = Column(JSON, default=list)
    summary = Column(Text, default="")
    model_used = Column(String(50), default="mock")
    created_at = Column(DateTime, default=datetime.utcnow)

    prompt = relationship("Prompt", back_populates="analyses")
