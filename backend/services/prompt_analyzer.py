"""
Servicio de análisis de prompts con IA.
Usa Anthropic si hay API key configurada, sino usa análisis heurístico.
"""
import os
import json
import re
from typing import Optional
from backend.services.prompt_criteria import CRITERIA, get_score_label

def _heuristic_analysis(content: str) -> dict:
    """Análisis heurístico cuando no hay API key disponible."""
    scores = {}
    suggestions = []
    strengths = []

    words = content.split()
    word_count = len(words)
    sentences = re.split(r'[.!?]+', content)
    has_newlines = '\n' in content
    has_examples = any(kw in content.lower() for kw in ['ejemplo', 'example', 'por ejemplo', 'e.g.', 'ej:'])
    has_role = any(kw in content.lower() for kw in ['actúa', 'actua', 'eres', 'you are', 'act as', 'rol'])
    has_format = any(kw in content.lower() for kw in ['lista', 'tabla', 'json', 'formato', 'format', 'bullet', 'párrafo', 'parrafo', 'markdown'])
    has_action_verb = any(kw in content.lower() for kw in ['analiza', 'redacta', 'resume', 'explica', 'crea', 'genera', 'lista', 'compara', 'describe', 'write', 'create', 'analyze', 'explain', 'list', 'summarize', 'compare'])
    has_restrictions = any(kw in content.lower() for kw in ['no ', 'evita', 'sin ', 'avoid', 'without', 'never', 'nunca', 'máximo', 'maximo', 'mínimo'])

    # Clarity
    clarity = 50.0
    if has_action_verb: clarity += 25
    if word_count > 10: clarity += 10
    if word_count > 30: clarity += 10
    if word_count > 5: clarity += 5
    clarity = min(clarity, 95)
    scores['clarity'] = clarity
    if clarity < 60:
        suggestions.append({
            "criterion": "Claridad",
            "issue": "El prompt carece de verbos de acción claros",
            "suggestion": "Comienza con un verbo específico: 'Analiza...', 'Redacta...', 'Crea...'",
            "priority": "high"
        })
    else:
        strengths.append("El objetivo del prompt es claro y directo")

    # Specificity
    specificity = 40.0
    if word_count > 20: specificity += 15
    if word_count > 50: specificity += 15
    if has_restrictions: specificity += 20
    if word_count > 100: specificity += 10
    specificity = min(specificity, 95)
    scores['specificity'] = specificity
    if specificity < 60:
        suggestions.append({
            "criterion": "Especificidad",
            "issue": "El prompt es demasiado genérico",
            "suggestion": "Añade restricciones: longitud esperada, tono, audiencia objetivo",
            "priority": "high"
        })
    else:
        strengths.append("El prompt incluye restricciones y detalles suficientes")

    # Structure
    structure = 50.0
    if has_newlines: structure += 30
    if len(sentences) > 2: structure += 15
    if word_count > 50 and has_newlines: structure += 10
    structure = min(structure, 95)
    scores['structure'] = structure
    if structure < 60:
        suggestions.append({
            "criterion": "Estructura",
            "issue": "El prompt es un bloque de texto sin estructura",
            "suggestion": "Divide el prompt en secciones con saltos de línea: contexto, tarea, formato",
            "priority": "medium"
        })

    # Format
    fmt = 30.0
    if has_format: fmt += 50
    if has_action_verb and has_format: fmt += 15
    fmt = min(fmt, 95)
    scores['format'] = fmt
    if fmt < 50:
        suggestions.append({
            "criterion": "Formato de salida",
            "issue": "No se especifica el formato de la respuesta esperada",
            "suggestion": "Indica el formato: 'Responde en formato lista', 'Usa markdown', 'Devuelve JSON con campos...'",
            "priority": "medium"
        })
    else:
        strengths.append("Se especifica claramente el formato de salida")

    # Context
    context = 40.0
    if has_role: context += 35
    if word_count > 30: context += 15
    if word_count > 80: context += 10
    context = min(context, 95)
    scores['context'] = context
    if context < 55:
        suggestions.append({
            "criterion": "Contexto",
            "issue": "El prompt carece de contexto suficiente",
            "suggestion": "Define el rol del modelo ('Actúa como experto en...') y el propósito final",
            "priority": "medium"
        })
    else:
        strengths.append("El contexto está bien definido")

    # Examples
    examples = 10.0
    if has_examples: examples = 85.0
    scores['examples'] = examples
    if examples < 50:
        suggestions.append({
            "criterion": "Ejemplos (Few-shot)",
            "issue": "No hay ejemplos que guíen al modelo",
            "suggestion": "Añade 1-2 ejemplos de input/output para tareas complejas o de formato específico",
            "priority": "low"
        })
    else:
        strengths.append("Incluye ejemplos que guían la respuesta")

    # Weighted overall score
    overall = sum(
        scores[k] * CRITERIA[k]['weight']
        for k in CRITERIA
    )

    label_info = get_score_label(overall)
    summary = f"Análisis heurístico: tu prompt obtiene una puntuación de {overall:.0f}/100 ({label_info['label']}). "
    if overall >= 75:
        summary += "El prompt está bien construido. "
    elif overall >= 55:
        summary += "El prompt es funcional pero tiene margen de mejora notable. "
    else:
        summary += "El prompt necesita mejoras importantes para ser efectivo. "
    summary += "Configura una API key de Anthropic para un análisis semántico completo."

    return {
        "overall_score": round(overall, 1),
        "criteria_scores": {k: round(v, 1) for k, v in scores.items()},
        "suggestions": suggestions,
        "strengths": strengths if strengths else ["El prompt tiene una base funcional"],
        "summary": summary,
        "model_used": "heuristic"
    }


async def _anthropic_analysis(content: str, api_key: str) -> dict:
    """Análisis semántico completo usando Anthropic."""
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)

        system_prompt = """Eres un experto en ingeniería de prompts para modelos de IA. 
Tu tarea es analizar la calidad de prompts y devolver ÚNICAMENTE un objeto JSON válido, sin texto adicional.

Evalúa estos 6 criterios con puntuaciones del 0 al 100:
- clarity: ¿El objetivo es claro y sin ambigüedad?
- specificity: ¿Hay suficiente detalle y restricciones?
- structure: ¿Tiene organización lógica?
- format: ¿Se especifica el formato de salida?
- context: ¿Provee contexto necesario al modelo?
- examples: ¿Incluye ejemplos few-shot?

Devuelve exactamente este JSON:
{
  "overall_score": <número 0-100>,
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
      "criterion": "<nombre>",
      "issue": "<problema concreto>",
      "suggestion": "<mejora específica y accionable>",
      "priority": "<high|medium|low>"
    }
  ],
  "strengths": ["<punto fuerte 1>", "<punto fuerte 2>"],
  "summary": "<resumen de 2-3 frases del análisis>"
}"""

        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1500,
            system=system_prompt,
            messages=[{"role": "user", "content": f"Analiza este prompt:\n\n{content}"}]
        )

        response_text = message.content[0].text.strip()
        # Clean potential markdown fences
        response_text = re.sub(r'^```json\s*', '', response_text)
        response_text = re.sub(r'\s*```$', '', response_text)

        result = json.loads(response_text)
        result["model_used"] = "claude-3-5-sonnet"
        return result

    except Exception as e:
        # Fall back to heuristic
        result = _heuristic_analysis(content)
        result["summary"] = f"Error con API Anthropic ({str(e)[:60]}). " + result["summary"]
        return result


async def analyze_prompt(content: str, api_key: Optional[str] = None) -> dict:
    """
    Analiza un prompt y devuelve puntuaciones y sugerencias.
    Usa Anthropic si hay API key, sino análisis heurístico.
    """
    if api_key and api_key.strip().startswith("sk-ant-"):
        return await _anthropic_analysis(content, api_key.strip())
    else:
        return _heuristic_analysis(content)
