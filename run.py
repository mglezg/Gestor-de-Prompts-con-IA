#!/usr/bin/env python3
"""
Script de arranque del Gestor de Prompts.
Ejecuta: python run.py
"""
import uvicorn
import os
import sys

# Ensure project root is in Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Create data directory if not exists
os.makedirs("data", exist_ok=True)

if __name__ == "__main__":
    print("\n" + "="*50)
    print("  🚀 Prompt Manager - Iniciando servidor...")
    print("="*50)
    print("  📡 URL: http://localhost:8000")
    print("  📚 API docs: http://localhost:8000/docs")
    print("  Ctrl+C para detener")
    print("="*50 + "\n")

    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=["backend"]
    )
