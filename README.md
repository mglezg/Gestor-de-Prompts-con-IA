# ⚡ Prompt Manager

**Gestor de prompts para modelos de inteligencia artificial con análisis de calidad por IA.**

Prompt Manager es una aplicación web local que te permite organizar, versionar y analizar la calidad de tus prompts para modelos de IA como Claude, GPT-4, DeepSeek y otros. Incluye un motor de análisis heurístico integrado y soporte para análisis semántico avanzado mediante Anthropic, OpenAI y DeepSeek.

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
- [Configuración de proveedores IA](#-configuración-de-proveedores-ia)
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
- 🤖 **Tres proveedores IA** — análisis semántico con Anthropic, OpenAI o DeepSeek (seleccionable)
- 🕐 **Control de versiones** — historial completo de cambios con posibilidad de restaurar versiones anteriores
- ⇔ **Comparador** — compara dos prompts lado a lado con análisis paralelo
- 🔍 **Búsqueda avanzada** — búsqueda en tiempo real por título, contenido y descripción
- 🏷️ **Sistema de tags** — etiqueta y filtra prompts por categorías
- 📦 **Exportar / Importar** — formato `.json` portable y compatible entre instalaciones
- 💾 **API keys persistentes** — las claves se guardan localmente en `data/.env.keys` y se cargan automáticamente al arrancar
- 🌙 **Interfaz oscura** — diseño profesional optimizado para uso prolongado
- 🖥️ **100% local** — no requiere conexión a internet para funcionar (salvo el análisis con IA)

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
| Python | **3.12** (recomendado) |
| RAM | 256 MB libres |
| Espacio en disco | 100 MB |
| Navegador | Chrome 90+, Firefox 88+, Edge 90+, Safari 15+ |
| Conexión a internet | Solo para análisis con IA (opcional) |

> ⚠️ **Python 3.13 y 3.14 no están soportados** actualmente debido a incompatibilidades con `pydantic-core`. Se recomienda Python 3.12.

---

## 🚀 Instalación

### Paso 1 — Descargar el proyecto

Descarga o clona el repositorio en tu máquina:

```bash
git clone https://github.com/mglezg/Gestor-de-Prompts-con-IA.git
cd Gestor-de-Prompts-con-IA
```

O descomprime el archivo `.zip` descargado y accede a la carpeta desde la terminal.

---

### Paso 2 — Python 3.12

El `setup.cmd` gestiona la instalación de Python automáticamente. Si tienes el instalador `python-3.12.x-amd64.exe` en la carpeta del proyecto, lo ejecutará en silencio. Si no, abrirá la página de descarga oficial:

[https://www.python.org/downloads/release/python-31210/](https://www.python.org/downloads/release/python-31210/)

Durante la instalación manual marca siempre **"Add Python to PATH"**.

---

### Paso 3 — Ejecutar el setup automático

#### En Windows

Haz doble clic en `setup.cmd` o ejecútalo desde la terminal:

```cmd
setup.cmd
```

Este script realiza automáticamente:
1. Búsqueda del instalador de Python en la carpeta del proyecto (si no hay Python en el sistema)
2. Verificación de la versión de Python instalada
3. Eliminación del entorno virtual anterior (si existe)
4. Creación de un entorno virtual limpio en `.venv`
5. Actualización de `pip`, `setuptools` y `wheel`
6. Instalación de todas las dependencias desde `requirements.txt`

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

El script activa el entorno virtual, abre automáticamente el navegador en `http://localhost:8000` y lanza el servidor.

#### En macOS / Linux

```bash
source .venv/bin/activate
python run.py
```

Luego abre tu navegador en [http://localhost:8000](http://localhost:8000).

---

### Actualizar dependencias

Si has recibido una nueva versión del proyecto y necesitas reinstalar desde cero, usa `update.cmd`:

```cmd
update.cmd
```

Este script elimina siempre el entorno virtual existente y lo recrea de cero, garantizando que no queden versiones antiguas de ningún paquete.

---

### Instalación manual (sin scripts)

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
# Lanzar (Windows)
start.cmd

# Lanzar (macOS/Linux)
python run.py

# Detener
Ctrl + C en la terminal
```

---

## 📁 Estructura del proyecto

```
Gestor-de-Prompts-con-IA/
│
├── 📄 run.py                        # Script de arranque del servidor
├── 📄 requirements.txt              # Dependencias Python
├── 📄 start.cmd                     # Lanzador Windows (abre navegador automáticamente)
├── 📄 setup.cmd                     # Setup automático Windows
├── 📄 update.cmd                    # Reinstalación limpia de dependencias
├── 📄 README.md                     # Este archivo
├── 📄 LICENSE                       # Licencia Apache 2.0
├── 📄 NOTICE                        # Aviso de autoría y atribución
├── 📄 SECURITY.md                   # Política de seguridad y reporte de vulnerabilidades
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
│   │   └── ai_analysis.py           # Análisis IA + configuración de proveedores
│   │
│   ├── 📂 services/                 # Lógica de negocio
│   │   ├── prompt_analyzer.py       # Motor de análisis (heurístico + Anthropic + OpenAI + DeepSeek)
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
    ├── prompts.db                   # Base de datos SQLite (se crea automáticamente)
    └── .env.keys                    # API keys persistidas localmente (no subir al repositorio)
```

---

## 🔧 Funcionalidades en detalle

### Gestión de proyectos

- Crea proyectos con nombre, descripción, icono emoji y color personalizado
- Filtra todos los prompts por proyecto desde el panel lateral
- Visualiza el número de prompts por proyecto en el dashboard
- Edita o elimina proyectos desde la interfaz

### Editor de prompts

- Editor de texto con fuente monoespaciada optimizada para prompts
- Conteo de palabras en tiempo real
- Selector de **modelo objetivo** (Claude, GPT-4, Gemini, Llama, etc.)
- Asignación de **tags** separados por coma para categorización
- **Nota de versión** para documentar cada cambio guardado
- Los cambios en el contenido generan automáticamente una nueva versión

### Control de versiones

Cada vez que guardas un prompt con contenido modificado se crea una nueva versión automáticamente. Desde el botón **🕐 Historial** puedes ver todas las versiones, previsualizar cualquiera y restaurar una versión anterior.

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

El análisis devuelve puntuación global, barras por criterio, fortalezas detectadas y sugerencias priorizadas (alta / media / baja).

Sin API key de ningún proveedor, el análisis es **heurístico** (basado en patrones lingüísticos). Con API key configurada, el análisis es **semántico** y evalúa el significado real del prompt.

### Comparador de prompts

Selecciona dos prompts y obtén un análisis paralelo lado a lado para identificar cuál está mejor construido y en qué criterios difieren.

### Búsqueda y filtrado

- Búsqueda global en tiempo real (título, contenido y descripción)
- Filtro por proyecto desde el panel lateral
- Filtro por tag con chips clicables
- Ambos filtros son combinables

---

## 🌐 API REST

La documentación interactiva completa está disponible en:

```
http://localhost:8000/docs
```

### Endpoints principales

#### Proyectos
```
GET    /api/projects/                Lista todos los proyectos
POST   /api/projects/                Crea un proyecto
GET    /api/projects/{id}            Obtiene un proyecto
PUT    /api/projects/{id}            Actualiza un proyecto
DELETE /api/projects/{id}            Elimina un proyecto
```

#### Prompts
```
GET    /api/prompts/                 Lista prompts (con filtros opcionales)
POST   /api/prompts/                 Crea un prompt
GET    /api/prompts/{id}             Obtiene un prompt
PUT    /api/prompts/{id}             Actualiza un prompt (versiona automáticamente)
DELETE /api/prompts/{id}             Elimina un prompt
GET    /api/prompts/{id}/versions    Historial de versiones
POST   /api/prompts/{id}/restore/{v} Restaura una versión
GET    /api/prompts/export/json      Exporta prompts a JSON
POST   /api/prompts/import/json      Importa prompts desde JSON
GET    /api/prompts/meta/tags        Lista todos los tags únicos
```

#### Análisis
```
POST   /api/analysis/analyze              Analiza un prompt (por id o contenido directo)
POST   /api/analysis/quick                Análisis rápido sin guardar
GET    /api/analysis/prompt/{id}          Historial de análisis de un prompt
GET    /api/analysis/criteria             Definición de criterios
POST   /api/analysis/config/api-key       Configura la API key de un proveedor
GET    /api/analysis/config/providers     Estado y modelos de los tres proveedores
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

# Analizar con DeepSeek
curl -X POST http://localhost:8000/api/analysis/analyze \
  -H "Content-Type: application/json" \
  -d '{"prompt_id": 1, "provider": "deepseek", "model": "deepseek-chat"}'
```

---

## 🤖 Configuración de proveedores IA

La aplicación soporta tres proveedores para el análisis semántico. Ve a **⚙ Configuración** en el sidebar para gestionarlos.

### Proveedores disponibles

| Proveedor | Modelos disponibles | Dónde obtener la key |
|---|---|---|
| **Anthropic** | claude-3-5-sonnet, claude-3-5-haiku, claude-3-opus... | [console.anthropic.com](https://console.anthropic.com) |
| **OpenAI** | gpt-4o, gpt-4o-mini, gpt-4-turbo, gpt-3.5-turbo | [platform.openai.com/api-keys](https://platform.openai.com/api-keys) |
| **DeepSeek** | deepseek-chat, deepseek-reasoner | [platform.deepseek.com/api_keys](https://platform.deepseek.com/api_keys) |

### Cómo configurar

1. Ve a **⚙ Configuración**
2. Introduce la API key del proveedor deseado
3. Selecciona el modelo con el que quieres analizar
4. Haz clic en **Guardar** — la tarjeta del proveedor se pondrá en verde confirmando que está activa
5. Elige el **proveedor activo** con los botones Auto / Anthropic / OpenAI / DeepSeek

### Persistencia de las keys

Las API keys se guardan automáticamente en `data/.env.keys` (solo en tu equipo, nunca sale del proyecto). Al reiniciar el servidor se cargan de forma automática — no hace falta introducirlas de nuevo.

> ⚠️ Añade `data/.env.keys` a tu `.gitignore` para que nunca se suba al repositorio.

### Modo Auto

Si seleccionas **Auto**, el sistema usa el primer proveedor que encuentre con key configurada, en este orden de preferencia: Anthropic → OpenAI → DeepSeek. Sin ninguna key activa se usa el análisis heurístico.

---

## 📦 Exportar e importar prompts

### Exportar

Desde la vista **Todos los prompts**, haz clic en **↓ Exportar**. Se descargará un archivo `.json`:

```json
{
  "format_version": "1.0",
  "app": "PromptManager",
  "exported_at": "2026-03-01T10:00:00",
  "prompts": [
    {
      "title": "Nombre del prompt",
      "content": "Contenido...",
      "description": "Para qué sirve",
      "tags": ["tag1", "tag2"],
      "model_target": "deepseek-chat",
      "version": 3,
      "created_at": "2026-01-15T09:00:00"
    }
  ]
}
```

### Importar

Haz clic en **↑ Importar** y selecciona un archivo `.json` exportado previamente. Los prompts se importarán sin proyecto asignado; puedes asignarlos manualmente después.

> 📌 El formato es compatible entre distintas instalaciones de Prompt Manager.

---

## 📊 Criterios de calidad

### Claridad (20%)
- ✅ Usa verbos de acción específicos: *analiza, redacta, resume, crea, compara...*
- ❌ Evita instrucciones vagas: *"hazlo mejor"*, *"algo sobre X"*

### Especificidad (20%)
- ✅ Define longitud, tono, audiencia, restricciones
- ✅ Especifica qué NO debe hacer el modelo si aplica

### Estructura (15%)
- ✅ Separa contexto, instrucción y formato con saltos de línea
- ✅ Coloca la instrucción principal al final para mayor énfasis

### Formato de salida (20%)
- ✅ Indica formato: lista, párrafos, tabla, JSON, markdown...
- ✅ Especifica nivel de detalle (resumen ejecutivo vs. análisis profundo)

### Contexto (15%)
- ✅ Define el rol del modelo: *"Actúa como experto en..."*
- ✅ Menciona el propósito final del output

### Ejemplos / Few-shot (10%)
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
No. Todo se guarda localmente en `data/prompts.db` (SQLite). Las únicas comunicaciones externas son las llamadas a las APIs de IA cuando el usuario las configura explícitamente.

**¿Puedo usar la aplicación sin API key?**
Sí. Sin ninguna key activa se usa el motor de análisis heurístico, que evalúa el prompt mediante patrones lingüísticos. Es útil para detectar problemas estructurales básicos.

**¿Las API keys se guardan de forma segura?**
Se guardan en `data/.env.keys`, un archivo local en tu equipo que nunca se envía a ningún servidor. Asegúrate de añadirlo a `.gitignore` si trabajas con un repositorio git.

**¿Qué ocurre si elimino un proyecto?**
Los prompts del proyecto no se eliminan; quedan sin proyecto asignado y siguen apareciendo en "Todos los prompts".

**¿Puedo hacer backup de mis datos?**
Sí. Copia `data/prompts.db` a un lugar seguro. También puedes usar la función de exportación para guardar tus prompts en formato JSON portable.

**¿Puedo ejecutar varias instancias a la vez?**
No en el mismo puerto. Cambia el puerto en `run.py` si necesitas otra instancia:
```python
uvicorn.run("backend.main:app", host="0.0.0.0", port=8001, ...)
```

**¿Cómo actualizo las dependencias tras una nueva versión?**
Ejecuta `update.cmd` en Windows. Este script elimina el entorno virtual anterior y lo recrea desde cero con las versiones correctas.

---

## 🛠️ Tecnologías utilizadas

| Capa | Tecnología | Versión |
|---|---|---|
| Backend | [FastAPI](https://fastapi.tiangolo.com/) | 0.115+ |
| Servidor ASGI | [Uvicorn](https://www.uvicorn.org/) | 0.30+ |
| ORM | [SQLAlchemy](https://www.sqlalchemy.org/) | 2.0+ |
| Base de datos | SQLite | (incluida en Python) |
| Validación | [Pydantic](https://docs.pydantic.dev/) | 2.9+ |
| IA — Anthropic | [Anthropic SDK](https://github.com/anthropics/anthropic-sdk-python) | 0.34+ |
| IA — OpenAI | [OpenAI SDK](https://github.com/openai/openai-python) | <1.45 |
| IA — DeepSeek | httpx (llamada directa) | 0.27+ |
| Frontend | HTML5 + CSS3 + JavaScript vanilla | — |
| Fuentes | Syne, DM Mono, Inter (Google Fonts) | — |

---

## 📄 Licencia

Este proyecto está distribuido bajo la **Licencia Apache 2.0**.

```
Copyright 2026 Miguel González González

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

La Licencia Apache 2.0 permite el uso, copia, modificación y distribución de este software, siempre que se cumplan las siguientes condiciones:

- Se debe conservar el aviso de copyright original de **Miguel González González** en todas las copias o partes sustanciales del software.
- Las obras derivadas deben incluir un aviso claro indicando que el archivo original ha sido modificado.
- No se puede usar el nombre del autor para promocionar productos derivados sin permiso expreso por escrito.
- Si el proyecto incluye un archivo `NOTICE`, este debe conservarse en cualquier redistribución.

El texto completo de la licencia se encuentra en el archivo [`LICENSE`](./LICENSE) de este repositorio.

> ⚠️ El incumplimiento de estos términos puede constituir una infracción de los derechos de propiedad intelectual del autor y ser perseguible conforme a la legislación aplicable.

---

<div align="center">
  <strong>⚡ Prompt Manager</strong> — Desarrollado por Miguel González González<br>
  <sub>Hecho para ingenieros de prompts y usuarios de IA</sub>
</div>
