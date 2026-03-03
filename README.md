# ⚡ Prompt Manager

**Gestor de prompts para modelos de inteligencia artificial con análisis de calidad por IA.**

Prompt Manager es una aplicación web local que te permite organizar, versionar y analizar la calidad de tus prompts para modelos de IA como Claude, GPT-4, Gemini y otros. Incluye un motor de análisis heurístico integrado y soporte opcional para análisis semántico avanzado mediante la API de Anthropic.

---

## 📋 Tabla de contenidos

- [Características](#-características)
- [Capturas de pantalla](#-capturas-de-pantalla)
- [Requisitos del sistema](#-requisitos-del-sistema)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Estructura del proyecto](#-estructura-del-proyecto)
- [Funcionalidades en detalle](#-funcionalidades-en-detalle)
- [API REST](#-api-rest)
- [Configuración de API Key de Anthropic](#-configuración-de-api-key-de-anthropic)
- [Exportar e importar prompts](#-exportar-e-importar-prompts)
- [Criterios de calidad](#-criterios-de-calidad)
- [Preguntas frecuentes](#-preguntas-frecuentes)
- [Tecnologías utilizadas](#-tecnologías-utilizadas)
- [Licencia](#-licencia)

---

## ✨ Características

- 📁 **Gestión por proyectos** — organiza tus prompts en proyectos con color e icono personalizado
- ✏️ **Editor de prompts** — editor con conteo de palabras, tags, modelo objetivo y notas de versión
- 🔬 **Análisis de calidad IA** — evaluación automática en 6 criterios con puntuación 0–100
- 🕐 **Control de versiones** — historial completo de cambios con posibilidad de restaurar versiones anteriores
- ⇔ **Comparador** — compara dos prompts lado a lado con análisis paralelo
- 🔍 **Búsqueda avanzada** — búsqueda en tiempo real por título, contenido y descripción
- 🏷️ **Sistema de tags** — etiqueta y filtra prompts por categorías
- 📦 **Exportar / Importar** — formato `.json` portable y compatible entre instalaciones
- 🌙 **Interfaz oscura** — diseño profesional optimizado para uso prolongado
- 🖥️ **100% local** — no requiere conexión a internet para funcionar (salvo el análisis con Anthropic)

---

## 🖼️ Capturas de pantalla

```
┌─────────────────────────────────────────────────────────┐
│  SIDEBAR              │  DASHBOARD                      │
│                       │                                 │
│  ⚡ PromptMgr         │  ◈ 12 prompts  📁 4 proyectos  │
│                       │                                 │
│  ◈ Dashboard          │  Prompts recientes              │
│  ≡ Todos los prompts  │  ├ Prompt de resumen    v3      │
│  ⇔ Comparar           │  ├ Extractor de datos   v1      │
│  ◎ Guía criterios     │  └ Generador de código  v2      │
│                       │                                 │
│  PROYECTOS            │  Proyectos                      │
│  ● Marketing          │  ● Marketing      · 4 prompts  │
│  ● Desarrollo         │  ● Desarrollo     · 5 prompts  │
│  ● Investigación      │  ● Investigación  · 3 prompts  │
│                       │                                 │
│  ⚙ Configuración      │                                 │
└─────────────────────────────────────────────────────────┘
```

---

## 💻 Requisitos del sistema

| Componente | Requisito mínimo |
|---|---|
| Sistema operativo | Windows 10/11, macOS 12+, Linux (Ubuntu 20.04+) |
| Python | **3.11 o 3.12** (recomendado) |
| RAM | 256 MB libres |
| Espacio en disco | 100 MB |
| Navegador | Chrome 90+, Firefox 88+, Edge 90+, Safari 15+ |
| Conexión a internet | Solo para análisis con Anthropic (opcional) |

> ⚠️ **Python 3.13 y 3.14 no están soportados** actualmente debido a incompatibilidades con `pydantic-core`. Usa Python 3.11 o 3.12.

---

## 🚀 Instalación

### Paso 1 — Descargar el proyecto

Descarga o clona el repositorio en tu máquina:

```bash
git clone https://github.com/tu-usuario/prompt-manager.git
cd prompt-manager
```

O descomprime el archivo `.zip` descargado y accede a la carpeta desde la terminal.

---

### Paso 2 — Instalar Python 3.11 o 3.12

Si aún no tienes Python instalado:

- Descarga desde [python.org](https://www.python.org/downloads/)
- Durante la instalación en Windows, **marca la casilla "Add Python to PATH"**
- Verifica la instalación:

```bash
python --version
# Debe mostrar Python 3.11.x o Python 3.12.x
```

---

### Paso 3 — Ejecutar el setup automático

#### En Windows

Haz doble clic en `setup.cmd` o ejecútalo desde la terminal:

```cmd
setup.cmd
```

Este script realizará automáticamente:
1. Verificación de Python en el sistema
2. Eliminación del entorno virtual anterior (si existe)
3. Creación de un entorno virtual limpio en `.venv`
4. Actualización de `pip`, `setuptools` y `wheel`
5. Instalación de todas las dependencias desde `requirements.txt`

#### En macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

---

### Paso 4 — Lanzar la aplicación

#### En Windows

Haz doble clic en `start.cmd` o ejecútalo desde la terminal:

```cmd
start.cmd
```

El script activará el entorno virtual, abrirá automáticamente el navegador en `http://localhost:8000` y lanzará el servidor.

#### En macOS / Linux

```bash
source .venv/bin/activate
python run.py
```

Luego abre tu navegador en [http://localhost:8000](http://localhost:8000).

---

### Instalación manual (sin scripts)

Si prefieres hacerlo paso a paso:

```bash
# Crear entorno virtual
python -m venv .venv

# Activar entorno (Windows)
.venv\Scripts\activate
# Activar entorno (macOS/Linux)
source .venv/bin/activate

# Actualizar herramientas base
pip install --upgrade pip setuptools wheel

# Instalar dependencias
pip install -r requirements.txt

# Arrancar
python run.py
```

---

## 🎯 Uso

### Primera vez

1. Abre la aplicación en [http://localhost:8000](http://localhost:8000)
2. Crea tu primer **proyecto** desde el panel lateral (botón `+` junto a "Proyectos")
3. Crea tu primer **prompt** con el botón `+ Nuevo prompt`
4. Escribe o pega el contenido del prompt en el editor
5. Haz clic en **🔬 Analizar** para obtener una evaluación de calidad

### Flujo de trabajo típico

```
Crear proyecto → Crear prompt → Editar → Analizar → Mejorar → Guardar versión
```

### Lanzar y detener el servidor

```cmd
# Lanzar
start.cmd           (Windows)
python run.py       (macOS/Linux)

# Detener
Ctrl + C en la terminal
```

---

## 📁 Estructura del proyecto

```
prompt-manager/
│
├── 📄 run.py                        # Script de arranque del servidor
├── 📄 requirements.txt              # Dependencias Python
├── 📄 start.cmd                     # Lanzador Windows (abre navegador automáticamente)
├── 📄 setup.cmd                     # Setup automático Windows
├── 📄 README.md                     # Este archivo
│
├── 📂 backend/                      # Servidor FastAPI
│   ├── main.py                      # Aplicación principal y rutas estáticas
│   ├── database.py                  # Configuración SQLite + SQLAlchemy
│   │
│   ├── 📂 models/                   # Modelos ORM (base de datos)
│   │   ├── project.py               # Modelo Proyecto
│   │   ├── prompt.py                # Modelos Prompt y PromptVersion
│   │   └── analysis.py              # Modelo Analysis
│   │
│   ├── 📂 routers/                  # Endpoints de la API REST
│   │   ├── projects.py              # CRUD de proyectos
│   │   ├── prompts.py               # CRUD de prompts + export/import
│   │   └── ai_analysis.py           # Análisis IA + configuración
│   │
│   ├── 📂 services/                 # Lógica de negocio
│   │   ├── prompt_analyzer.py       # Motor de análisis (heurístico + Anthropic)
│   │   └── prompt_criteria.py       # Definición de criterios de calidad
│   │
│   └── 📂 schemas/                  # Validación de datos (Pydantic)
│       ├── project.py
│       └── prompt.py
│
├── 📂 frontend/                     # Interfaz web
│   ├── index.html                   # Aplicación SPA principal
│   ├── 📂 css/
│   │   └── styles.css               # Estilos globales (tema oscuro)
│   └── 📂 js/
│       └── app.js                   # Lógica de la interfaz
│
└── 📂 data/
    └── prompts.db                   # Base de datos SQLite (se crea automáticamente)
```

---

## 🔧 Funcionalidades en detalle

### Gestión de proyectos

- Crea proyectos con nombre, descripción, icono emoji y color personalizado
- Filtra todos los prompts por proyecto desde el panel lateral
- Visualiza el número de prompts por proyecto en el dashboard
- Edita o elimina proyectos con doble clic en el nombre del proyecto

### Editor de prompts

- Editor de texto con fuente monoespaciada optimizada para prompts
- Conteo de palabras en tiempo real
- Selector de **modelo objetivo** (Claude, GPT-4, Gemini, Llama, etc.)
- Asignación de **tags** separados por coma para categorización
- **Nota de versión** para documentar cada cambio guardado
- Los cambios en el contenido generan automáticamente una nueva versión

### Control de versiones

Cada vez que guardas un prompt con contenido modificado, se crea una nueva versión automáticamente. Desde el botón **🕐 Historial** puedes:

- Ver todas las versiones con fecha y nota de cambio
- **Previsualizar** cualquier versión sin guardar
- **Restaurar** una versión anterior (crea una nueva versión con el contenido antiguo)

### Análisis de calidad IA

El motor de análisis evalúa 6 criterios y devuelve una puntuación de 0 a 100:

| Criterio | Peso | Descripción |
|---|---|---|
| Claridad | 20% | ¿El objetivo del prompt es claro y sin ambigüedad? |
| Especificidad | 20% | ¿Hay suficiente detalle y restricciones? |
| Estructura | 15% | ¿Tiene organización lógica y fluida? |
| Formato de salida | 20% | ¿Se especifica cómo debe ser la respuesta? |
| Contexto | 15% | ¿Provee el contexto necesario al modelo? |
| Ejemplos (Few-shot) | 10% | ¿Incluye ejemplos que guíen al modelo? |

El análisis devuelve:
- **Puntuación global** con indicador visual (Excelente / Muy bueno / Bueno / Mejorable / Débil)
- **Barras de criterio** individuales
- **Fortalezas** identificadas en el prompt
- **Sugerencias** priorizadas (alta / media / baja) con el problema concreto y la mejora recomendada

Sin API Key de Anthropic, el análisis es **heurístico** (basado en patrones lingüísticos). Con API Key, el análisis es **semántico** usando Claude 3.5 Sonnet.

### Comparador de prompts

Selecciona dos prompts de tus colecciones y obtén un análisis paralelo lado a lado. El comparador indica cuál de los dos obtiene mejor puntuación global y muestra las barras de criterios de ambos para identificar diferencias.

### Búsqueda y filtrado

- **Búsqueda global** en tiempo real desde la barra superior (busca en título, contenido y descripción)
- **Filtro por proyecto** desde el panel lateral
- **Filtro por tag** con chips clicables encima de la lista de prompts
- Ambos filtros son combinables

---

## 🌐 API REST

La aplicación expone una API REST completa. Puedes consultarla en:

```
http://localhost:8000/docs
```

### Endpoints principales

#### Proyectos
```
GET    /api/projects/              Lista todos los proyectos
POST   /api/projects/              Crea un proyecto
GET    /api/projects/{id}          Obtiene un proyecto
PUT    /api/projects/{id}          Actualiza un proyecto
DELETE /api/projects/{id}          Elimina un proyecto
```

#### Prompts
```
GET    /api/prompts/               Lista prompts (con filtros opcionales)
POST   /api/prompts/               Crea un prompt
GET    /api/prompts/{id}           Obtiene un prompt
PUT    /api/prompts/{id}           Actualiza un prompt (versiona automáticamente)
DELETE /api/prompts/{id}           Elimina un prompt
GET    /api/prompts/{id}/versions  Historial de versiones
POST   /api/prompts/{id}/restore/{v} Restaura una versión
GET    /api/prompts/export/json    Exporta prompts a JSON
POST   /api/prompts/import/json    Importa prompts desde JSON
GET    /api/prompts/meta/tags      Lista todos los tags únicos
```

#### Análisis
```
POST   /api/analysis/analyze       Analiza un prompt (por id o contenido directo)
POST   /api/analysis/quick         Análisis rápido sin guardar
GET    /api/analysis/prompt/{id}   Historial de análisis de un prompt
GET    /api/analysis/criteria      Definición de criterios
POST   /api/analysis/config/api-key       Configura la API key de Anthropic
GET    /api/analysis/config/api-key-status Estado de la API key
```

### Ejemplo de uso con curl

```bash
# Crear un proyecto
curl -X POST http://localhost:8000/api/projects/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Mi proyecto", "color": "#3b82f6", "icon": "🚀"}'

# Crear un prompt
curl -X POST http://localhost:8000/api/prompts/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Mi primer prompt", "content": "Actúa como...", "tags": ["util"]}'

# Analizar un prompt
curl -X POST http://localhost:8000/api/analysis/analyze \
  -H "Content-Type: application/json" \
  -d '{"prompt_id": 1}'
```

---

## 🤖 Configuración de API Key de Anthropic

Por defecto, el análisis es **heurístico** y no requiere conexión a internet. Para activar el análisis semántico con Claude:

1. Obtén una API key en [console.anthropic.com](https://console.anthropic.com)
2. En la aplicación, ve a **⚙ Configuración**
3. Introduce tu API key (formato `sk-ant-api03-...`)
4. Haz clic en **Guardar API key**
5. El indicador verde en el sidebar confirma que está activa

> ⚠️ La API key se guarda en memoria mientras el servidor está activo. Al reiniciar el servidor, deberás introducirla de nuevo. Para persistirla, puedes definirla como variable de entorno:

```bash
# Windows
set ANTHROPIC_API_KEY=sk-ant-api03-...

# macOS / Linux
export ANTHROPIC_API_KEY=sk-ant-api03-...
```

O añadirla al inicio de `run.py`:

```python
import os
os.environ["ANTHROPIC_API_KEY"] = "sk-ant-api03-..."
```

---

## 📦 Exportar e importar prompts

### Exportar

Desde la vista **Todos los prompts** (o desde un proyecto específico), haz clic en **↓ Exportar**. Se descargará un archivo `.json` con el siguiente formato:

```json
{
  "format_version": "1.0",
  "app": "PromptManager",
  "exported_at": "2025-03-01T10:00:00",
  "prompts": [
    {
      "title": "Nombre del prompt",
      "content": "Contenido...",
      "description": "Para qué sirve",
      "tags": ["tag1", "tag2"],
      "model_target": "claude-3-5-sonnet",
      "version": 3,
      "created_at": "2025-01-15T09:00:00"
    }
  ]
}
```

### Importar

Haz clic en **↑ Importar** y selecciona un archivo `.json` exportado previamente desde esta aplicación. Los prompts se importarán sin proyecto asignado; puedes asignarlos manualmente después.

> 📌 El formato de exportación es compatible entre distintas instalaciones de Prompt Manager, lo que permite compartir colecciones de prompts con otros usuarios.

---

## 📊 Criterios de calidad

El sistema evalúa cada prompt según estos 6 criterios. Puedes consultar la guía completa en la sección **◎ Guía de criterios** de la aplicación.

### Claridad (20%)
El prompt debe expresar su objetivo de forma directa y sin ambigüedad.
- ✅ Usa verbos de acción específicos: *analiza, redacta, resume, crea, compara...*
- ❌ Evita instrucciones vagas: *"hazlo mejor"*, *"algo sobre X"*

### Especificidad (20%)
El prompt debe incluir suficiente detalle para que el modelo no tenga que asumir.
- ✅ Define longitud, tono, audiencia, restricciones
- ✅ Especifica qué NO debe hacer el modelo si aplica

### Estructura (15%)
El prompt debe tener una organización lógica y fácil de seguir.
- ✅ Separa contexto, instrucción y formato con saltos de línea
- ✅ Coloca la instrucción principal al final para mayor énfasis

### Formato de salida (20%)
El modelo debe saber exactamente cómo debe presentar su respuesta.
- ✅ Indica formato: lista, párrafos, tabla, JSON, markdown...
- ✅ Especifica nivel de detalle (resumen ejecutivo vs. análisis profundo)

### Contexto (15%)
El prompt debe proveer la información de fondo que el modelo no puede inferir.
- ✅ Define el rol del modelo: *"Actúa como experto en..."*
- ✅ Menciona el propósito final del output

### Ejemplos / Few-shot (10%)
Los ejemplos son la herramienta más poderosa para prompts de formato específico.
- ✅ Incluye 1-3 pares input/output de ejemplo
- ✅ Añade ejemplos negativos para mostrar qué evitar

### Escala de puntuación

| Puntuación | Etiqueta |
|---|---|
| 90 – 100 | ✅ Excelente |
| 75 – 89 | 🟢 Muy bueno |
| 60 – 74 | 🟡 Bueno |
| 40 – 59 | 🟠 Mejorable |
| 0 – 39 | 🔴 Débil |

---

## ❓ Preguntas frecuentes

**¿Los datos se guardan en la nube?**
No. Todo se guarda localmente en el archivo `data/prompts.db` (SQLite). La aplicación no envía datos a ningún servidor excepto a la API de Anthropic si tienes configurada una API key y solicitas un análisis.

**¿Puedo usar la aplicación sin API key de Anthropic?**
Sí. Sin API key se activa el motor de análisis heurístico, que evalúa el prompt mediante patrones lingüísticos. La puntuación es orientativa pero útil para detectar problemas comunes.

**¿Qué ocurre si elimino un proyecto?**
Los prompts del proyecto no se eliminan; quedan sin proyecto asignado y siguen apareciendo en "Todos los prompts".

**¿Puedo hacer backup de mis datos?**
Sí. Copia el archivo `data/prompts.db` a un lugar seguro. También puedes usar la función de exportación para guardar tus prompts en formato JSON.

**¿La API key de Anthropic se persiste entre reinicios?**
No por defecto. Se guarda en memoria. Para persistirla, defínela como variable de entorno `ANTHROPIC_API_KEY` antes de lanzar el servidor (ver sección de configuración).

**¿Puedo ejecutar varias instancias a la vez?**
No en el mismo puerto. Si necesitas otra instancia, cambia el puerto en `run.py`:
```python
uvicorn.run("backend.main:app", host="0.0.0.0", port=8001, ...)
```

**¿Cómo actualizo las dependencias?**
Ejecuta `setup.cmd` de nuevo en Windows, o:
```bash
pip install --upgrade -r requirements.txt
```

---

## 🛠️ Tecnologías utilizadas

| Capa | Tecnología | Versión |
|---|---|---|
| Backend | [FastAPI](https://fastapi.tiangolo.com/) | 0.115+ |
| Servidor ASGI | [Uvicorn](https://www.uvicorn.org/) | 0.30+ |
| ORM | [SQLAlchemy](https://www.sqlalchemy.org/) | 2.0+ |
| Base de datos | SQLite | (incluida en Python) |
| Validación | [Pydantic](https://docs.pydantic.dev/) | 2.9+ |
| IA | [Anthropic SDK](https://github.com/anthropic/anthropic-sdk-python) | 0.34+ |
| Frontend | HTML5 + CSS3 + JavaScript vanilla | — |
| Fuentes | Syne, DM Mono, Inter (Google Fonts) | — |

---

## 📄 Licencia

Este proyecto se distribuye bajo licencia **MIT**.

```
MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

<div align="center">
  <strong>⚡ Prompt Manager</strong> — Hecho para ingenieros de prompts y usuarios de IA
</div>
