"""
Servicio de análisis de prompts con IA.
Soporta tres proveedores: Anthropic, OpenAI y DeepSeek.
Sin API key activa usa análisis heurístico.
"""
import os
import json
import re
from typing import Optional
from backend.services.prompt_criteria import CRITERIA, get_score_label

# ── Modelos disponibles por proveedor ────────────────────
PROVIDER_MODELS = {
    "anthropic": [
        "claude-sonnet-4-5",
        "claude-opus-4-5",
        "claude-3-5-sonnet-20241022",
        "claude-3-5-haiku-20241022",
        "claude-3-opus-20240229",
    ],
    "openai": [
        "gpt-4o",
        "gpt-4o-mini",
        "gpt-4-turbo",
        "gpt-4",
        "gpt-3.5-turbo",
    ],
    "deepseek": [
        "deepseek-chat",
        "deepseek-reasoner",
    ],
}

DEFAULT_MODELS = {
    "anthropic": "claude-3-5-sonnet-20241022",
    "openai":    "gpt-4o",
    "deepseek":  "deepseek-chat",
}

# ── System prompt compartido para todos los proveedores ──
ANALYSIS_SYSTEM_PROMPT = """Eres un experto en ingeniería de prompts para modelos de IA.
Tu tarea es analizar la calidad de prompts y devolver ÚNICAMENTE un objeto JSON válido, sin texto adicional, sin markdown, sin explicaciones.

Evalúa estos 6 criterios con puntuaciones del 0 al 100:
- clarity: El objetivo es claro y sin ambigüedad?
- specificity: Hay suficiente detalle y restricciones?
- structure: Tiene organización lógica?
- format: Se especifica el formato de salida?
- context: Provee contexto necesario al modelo?
- examples: Incluye ejemplos few-shot?

Devuelve exactamente este JSON y nada mas:
{
  "overall_score": <numero 0-100>,
  "criteria_scores": {
    "clarity": <0-100>,
    "specificity": <0-100>,
    "structure": <0-100>,
    "format": <0-100>,
    "context": <0-100>,
    "examples": <0-100>
  },
  "suggestions": [
    {
      "criterion": "<nombre del criterio>",
      "issue": "<problema concreto detectado>",
      "suggestion": "<mejora especifica y accionable>",
      "priority": "<high|medium|low>"
    }
  ],
  "strengths": ["<punto fuerte 1>", "<punto fuerte 2>"],
  "summary": "<resumen de 2-3 frases del analisis general>"
}"""


def _clean_json_response(text: str) -> str:
    """Limpia posibles markdown fences de la respuesta."""
    text = text.strip()
    text = re.sub(r'^```json\s*', '', text)
    text = re.sub(r'^```\s*', '', text)
    text = re.sub(r'\s*```$', '', text)
    return text.strip()


def _heuristic_analysis(content: str) -> dict:
    """Analisis heuristico cuando no hay API key disponible."""
    scores = {}
    suggestions = []
    strengths = []

    words = content.split()
    word_count = len(words)
    sentences = re.split(r'[.!?]+', content)
    has_newlines = '\n' in content
    has_examples = any(kw in content.lower() for kw in ['ejemplo', 'example', 'por ejemplo', 'e.g.', 'ej:'])
    has_role = any(kw in content.lower() for kw in ['actua', 'eres', 'you are', 'act as', 'rol'])
    has_format = any(kw in content.lower() for kw in ['lista', 'tabla', 'json', 'formato', 'format', 'bullet', 'parrafo', 'markdown'])
    has_action_verb = any(kw in content.lower() for kw in ['analiza', 'redacta', 'resume', 'explica', 'crea', 'genera', 'lista', 'compara', 'describe', 'write', 'create', 'analyze', 'explain', 'list', 'summarize', 'compare'])
    has_restrictions = any(kw in content.lower() for kw in ['no ', 'evita', 'sin ', 'avoid', 'without', 'never', 'nunca', 'maximo', 'minimo'])

    clarity = 50.0
    if has_action_verb: clarity += 25
    if word_count > 10: clarity += 10
    if word_count > 30: clarity += 10
    if word_count > 5:  clarity += 5
    clarity = min(clarity, 95)
    scores['clarity'] = clarity
    if clarity < 60:
        suggestions.append({"criterion": "Claridad", "issue": "El prompt carece de verbos de accion claros", "suggestion": "Comienza con un verbo especifico: 'Analiza...', 'Redacta...', 'Crea...'", "priority": "high"})
    else:
        strengths.append("El objetivo del prompt es claro y directo")

    specificity = 40.0
    if word_count > 20:  specificity += 15
    if word_count > 50:  specificity += 15
    if has_restrictions: specificity += 20
    if word_count > 100: specificity += 10
    specificity = min(specificity, 95)
    scores['specificity'] = specificity
    if specificity < 60:
        suggestions.append({"criterion": "Especificidad", "issue": "El prompt es demasiado generico", "suggestion": "Añade restricciones: longitud esperada, tono, audiencia objetivo", "priority": "high"})
    else:
        strengths.append("El prompt incluye restricciones y detalles suficientes")

    structure = 50.0
    if has_newlines:             structure += 30
    if len(sentences) > 2:       structure += 15
    if word_count > 50 and has_newlines: structure += 10
    structure = min(structure, 95)
    scores['structure'] = structure
    if structure < 60:
        suggestions.append({"criterion": "Estructura", "issue": "El prompt es un bloque de texto sin estructura", "suggestion": "Divide el prompt en secciones con saltos de linea: contexto, tarea, formato", "priority": "medium"})

    fmt = 30.0
    if has_format: fmt += 50
    if has_action_verb and has_format: fmt += 15
    fmt = min(fmt, 95)
    scores['format'] = fmt
    if fmt < 50:
        suggestions.append({"criterion": "Formato de salida", "issue": "No se especifica el formato de la respuesta esperada", "suggestion": "Indica el formato: 'Responde en formato lista', 'Usa markdown', 'Devuelve JSON con campos...'", "priority": "medium"})
    else:
        strengths.append("Se especifica claramente el formato de salida")

    context = 40.0
    if has_role:         context += 35
    if word_count > 30:  context += 15
    if word_count > 80:  context += 10
    context = min(context, 95)
    scores['context'] = context
    if context < 55:
        suggestions.append({"criterion": "Contexto", "issue": "El prompt carece de contexto suficiente", "suggestion": "Define el rol del modelo ('Actua como experto en...') y el proposito final", "priority": "medium"})
    else:
        strengths.append("El contexto esta bien definido")

    examples = 10.0
    if has_examples: examples = 85.0
    scores['examples'] = examples
    if examples < 50:
        suggestions.append({"criterion": "Ejemplos (Few-shot)", "issue": "No hay ejemplos que guien al modelo", "suggestion": "Añade 1-2 ejemplos de input/output para tareas complejas o de formato especifico", "priority": "low"})
    else:
        strengths.append("Incluye ejemplos que guian la respuesta")

    overall = sum(scores[k] * CRITERIA[k]['weight'] for k in CRITERIA)
    label_info = get_score_label(overall)
    summary = f"Analisis heuristico: puntuacion {overall:.0f}/100 ({label_info['label']}). "
    if overall >= 75:
        summary += "El prompt esta bien construido. "
    elif overall >= 55:
        summary += "El prompt es funcional pero tiene margen de mejora. "
    else:
        summary += "El prompt necesita mejoras importantes para ser efectivo. "
    summary += "Configura una API key para un analisis semantico completo."

    return {
        "overall_score": round(overall, 1),
        "criteria_scores": {k: round(v, 1) for k, v in scores.items()},
        "suggestions": suggestions,
        "strengths": strengths if strengths else ["El prompt tiene una base funcional"],
        "summary": summary,
        "model_used": "heuristic"
    }


async def _anthropic_analysis(content: str, api_key: str, model: str) -> dict:
    """Analisis semantico usando Anthropic."""
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        message = client.messages.create(
            model=model,
            max_tokens=1500,
            system=ANALYSIS_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": f"Analiza este prompt:\n\n{content}"}]
        )
        response_text = _clean_json_response(message.content[0].text)
        result = json.loads(response_text)
        result["model_used"] = f"anthropic/{model}"
        return result
    except Exception as e:
        result = _heuristic_analysis(content)
        result["summary"] = f"Error con Anthropic ({str(e)[:80]}). " + result["summary"]
        return result


async def _openai_analysis(content: str, api_key: str, model: str) -> dict:
    """Analisis semantico usando OpenAI."""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=model,
            max_tokens=1500,
            messages=[
                {"role": "system", "content": ANALYSIS_SYSTEM_PROMPT},
                {"role": "user",   "content": f"Analiza este prompt:\n\n{content}"}
            ],
            response_format={"type": "json_object"}
        )
        response_text = _clean_json_response(response.choices[0].message.content)
        result = json.loads(response_text)
        result["model_used"] = f"openai/{model}"
        return result
    except Exception as e:
        result = _heuristic_analysis(content)
        result["summary"] = f"Error con OpenAI ({str(e)[:80]}). " + result["summary"]
        return result


async def _deepseek_analysis(content: str, api_key: str, model: str) -> dict:
    """Analisis semantico usando DeepSeek (API compatible con OpenAI SDK)."""
    try:
        from openai import OpenAI
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com"
        )
        response = client.chat.completions.create(
            model=model,
            max_tokens=1500,
            messages=[
                {"role": "system", "content": ANALYSIS_SYSTEM_PROMPT},
                {"role": "user",   "content": f"Analiza este prompt:\n\n{content}"}
            ]
        )
        response_text = _clean_json_response(response.choices[0].message.content)
        result = json.loads(response_text)
        result["model_used"] = f"deepseek/{model}"
        return result
    except Exception as e:
        result = _heuristic_analysis(content)
        result["summary"] = f"Error con DeepSeek ({str(e)[:80]}). " + result["summary"]
        return result


async def analyze_prompt(
    content: str,
    api_key: Optional[str] = None,
    provider: Optional[str] = None,
    model: Optional[str] = None
) -> dict:
    """
    Analiza un prompt con el proveedor y modelo configurados.
    Si no hay API key activa, usa analisis heuristico.
    """
    if not api_key or not api_key.strip():
        return _heuristic_analysis(content)

    key = api_key.strip()

    if provider == "anthropic" or (not provider and key.startswith("sk-ant-")):
        m = model or DEFAULT_MODELS["anthropic"]
        return await _anthropic_analysis(content, key, m)

    elif provider == "openai":
        m = model or DEFAULT_MODELS["openai"]
        return await _openai_analysis(content, key, m)

    elif provider == "deepseek":
        m = model or DEFAULT_MODELS["deepseek"]
        return await _deepseek_analysis(content, key, m)

    elif not provider and key.startswith("sk-"):
        # Key de OpenAI sin proveedor explicito
        m = model or DEFAULT_MODELS["openai"]
        return await _openai_analysis(content, key, m)

    else:
        return _heuristic_analysis(content)
