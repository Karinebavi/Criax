@echo off
REM Abre o Esteira LIE no navegador (Windows).

cd /d "%~dp0"

if not exist ".venv" (
  echo ERRO: o ambiente ainda nao foi instalado.
  echo Rode primeiro:  instalar.bat
  pause
  exit /b 1
)

call .venv\Scripts\activate.bat

echo Abrindo o Esteira LIE no navegador...
echo Para fechar, volte aqui e aperte Ctrl + C.
streamlit run app\Home.py
