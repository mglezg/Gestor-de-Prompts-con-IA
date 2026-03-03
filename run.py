#!/usr/bin/env python3
"""
Script de arranque del Gestor de Prompts.
Ejecuta: python run.py
"""
import uvicorn
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.makedirs("data", exist_ok=True)

if __name__ == "__main__":
    print("\n" + "="*50)
    print("  Prompt Manager - Iniciando servidor...")
    print("="*50)
    print("  URL:      http://localhost:8000")
    print("  API docs: http://localhost:8000/docs")
    print("  Detener:  Ctrl+C")
    print("="*50 + "\n")

    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=False   # False: todo en un solo proceso, las API keys persisten en memoria
    )
