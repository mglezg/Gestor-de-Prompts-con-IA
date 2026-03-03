"""
Criterios de calidad para la evaluación de prompts de IA.
Estos criterios se usan tanto para el análisis automático como para guiar al usuario.
"""

CRITERIA = {
    "clarity": {
        "name": "Claridad",
        "description": "¿El objetivo del prompt es claro y sin ambigüedad?",
        "weight": 0.20,
        "tips": [
            "Usa verbos de acción específicos (analiza, redacta, lista, compara...)",
            "Evita instrucciones vagas como 'hazlo mejor' o 'algo sobre X'",
            "Una sola idea principal por prompt"
        ]
    },
    "specificity": {
        "name": "Especificidad",
        "description": "¿El prompt provee suficiente detalle y restricciones?",
        "weight": 0.20,
        "tips": [
            "Define longitud, formato o alcance esperado",
            "Incluye restricciones relevantes (idioma, tono, audiencia)",
            "Especifica qué NO debe hacer el modelo si aplica"
        ]
    },
    "structure": {
        "name": "Estructura",
        "description": "¿El prompt tiene una organización lógica y fluida?",
        "weight": 0.15,
        "tips": [
            "Separa el contexto de la instrucción principal",
            "Usa saltos de línea para dividir secciones largas",
            "Coloca la instrucción principal al final para mayor énfasis"
        ]
    },
    "format": {
        "name": "Formato de salida",
        "description": "¿Se especifica cómo debe ser la respuesta?",
        "weight": 0.20,
        "tips": [
            "Indica si quieres listas, párrafos, tablas, JSON, etc.",
            "Especifica el nivel de detalle (resumen vs. análisis profundo)",
            "Pide un formato consistente si habrá múltiples items"
        ]
    },
    "context": {
        "name": "Contexto",
        "description": "¿El prompt provee el contexto necesario al modelo?",
        "weight": 0.15,
        "tips": [
            "Define el rol del modelo si es relevante (ej: 'Actúa como...')",
            "Provee información de fondo que el modelo no puede asumir",
            "Menciona el propósito final del output"
        ]
    },
    "examples": {
        "name": "Ejemplos (Few-shot)",
        "description": "¿Incluye ejemplos que guíen al modelo?",
        "weight": 0.10,
        "tips": [
            "Añade 1-3 ejemplos de input/output esperado",
            "Los ejemplos son especialmente útiles para tareas de formato",
            "Usa ejemplos negativos para mostrar qué evitar"
        ]
    }
}

SCORE_LABELS = {
    (90, 100): {"label": "Excelente", "color": "#10b981"},
    (75, 90):  {"label": "Muy bueno", "color": "#6ee7b7"},
    (60, 75):  {"label": "Bueno",     "color": "#fbbf24"},
    (40, 60):  {"label": "Mejorable", "color": "#f97316"},
    (0, 40):   {"label": "Débil",     "color": "#ef4444"},
}

MODEL_TARGETS = [
    "general",
    "claude-3-5-sonnet",
    "claude-3-opus",
    "gpt-4o",
    "gpt-4-turbo",
    "gemini-1.5-pro",
    "llama-3",
    "mistral-large",
    "custom"
]

def get_score_label(score: float) -> dict:
    for (low, high), meta in SCORE_LABELS.items():
        if low <= score <= high:
            return meta
    return {"label": "Sin clasificar", "color": "#94a3b8"}
