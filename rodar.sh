#!/usr/bin/env bash
# Abre o Esteira LIE no navegador (Mac/Linux).

set -e
cd "$(dirname "$0")"

if [ ! -d ".venv" ]; then
  echo "ERRO: o ambiente ainda não foi instalado."
  echo "Rode primeiro:  ./instalar.sh"
  exit 1
fi

# shellcheck disable=SC1091
source .venv/bin/activate

echo "Abrindo o Esteira LIE no navegador..."
echo "Para fechar, volte aqui e aperte Ctrl + C."
streamlit run app/Home.py
