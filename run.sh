#!/bin/bash

# Script para executar o YouTube Downloader
# Certifica-se de que o ambiente virtual está ativado

cd "$(dirname "$0")"

# Ativa o ambiente virtual se existir
if [ -d ".venv" ]; then
    source .venv/bin/activate
    echo "✅ Ambiente virtual ativado"
else
    echo "⚠️  Ambiente virtual não encontrado. Execute primeiro:"
    echo "   python -m venv .venv"
    echo "   source .venv/bin/activate"
    echo "   pip install -r requirements.txt"
    exit 1
fi

# Verifica se as dependências estão instaladas
if ! python -c "import PyQt6" 2>/dev/null; then
    echo "⚠️  PyQt6 não está instalado. Instalando dependências..."
    pip install -r requirements.txt
fi

# Executa a aplicação
echo "🚀 Iniciando YouTube Downloader..."
python main.py
