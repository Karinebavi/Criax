#!/usr/bin/env bash
# Instalador do Esteira LIE (Mac/Linux).
# Cria o ambiente virtual .venv e instala as dependências.

set -e
cd "$(dirname "$0")"

echo "=============================================="
echo "  Instalando o Esteira LIE"
echo "=============================================="

# Procura um Python 3 disponível.
if command -v python3 >/dev/null 2>&1; then
  PY=python3
elif command -v python >/dev/null 2>&1; then
  PY=python
else
  echo "ERRO: Python não foi encontrado."
  echo "Instale o Python 3.11 ou superior em https://www.python.org/downloads/ e rode de novo."
  exit 1
fi

echo "Usando: $($PY --version)"

# Cria o ambiente virtual se ainda não existir.
if [ ! -d ".venv" ]; then
  echo "Criando ambiente virtual (.venv)..."
  "$PY" -m venv .venv
fi

# Ativa o ambiente e instala tudo.
# shellcheck disable=SC1091
source .venv/bin/activate
echo "Atualizando o pip..."
python -m pip install --upgrade pip
echo "Instalando as dependências (pode demorar alguns minutos)..."
python -m pip install -r requirements.txt

echo ""
echo "=============================================="
echo "  Pronto! Instalação concluída."
echo "  Agora rode:  ./rodar.sh"
echo "=============================================="
