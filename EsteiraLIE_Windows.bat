@echo off
REM ============================================================
REM   ESTEIRA LIE - Atalho unico para Windows
REM   Da dois cliques neste arquivo. Na primeira vez ele instala
REM   tudo (demora alguns minutos); nas proximas, so abre.
REM ============================================================
title Esteira LIE
cd /d "%~dp0"

REM Procura o Python.
where python >nul 2>nul
if %errorlevel%==0 (set PY=python) else (
  where py >nul 2>nul
  if %errorlevel%==0 (set PY=py) else (
    echo.
    echo  ERRO: Python nao foi encontrado.
    echo  1^) Baixe em https://www.python.org/downloads/
    echo  2^) Na instalacao, marque "Add Python to PATH"
    echo  3^) Depois rode este arquivo de novo.
    echo.
    pause
    exit /b 1
  )
)

REM Cria o ambiente virtual na primeira vez.
if not exist ".venv\Scripts\python.exe" (
  echo.
  echo  Primeira execucao: preparando o Esteira LIE...
  echo  Isso pode demorar alguns minutos. Nao feche esta janela.
  echo.
  %PY% -m venv .venv
)

REM Ativa o ambiente e SEMPRE confere as dependencias (rapido quando ja instaladas;
REM garante que novas bibliotecas entrem quando o sistema e atualizado).
call .venv\Scripts\activate.bat
echo  Conferindo as bibliotecas necessarias...
python -m pip install --upgrade pip >nul 2>nul
python -m pip install -r requirements.txt

REM Evita a pergunta de e-mail do Streamlit na primeira execucao.
if not exist "%USERPROFILE%\.streamlit" mkdir "%USERPROFILE%\.streamlit"
if not exist "%USERPROFILE%\.streamlit\credentials.toml" (
  > "%USERPROFILE%\.streamlit\credentials.toml" echo [general]
  >> "%USERPROFILE%\.streamlit\credentials.toml" echo email = ""
)

echo.
echo  Abrindo o Esteira LIE no seu navegador...
echo  Para FECHAR o sistema, feche esta janela preta.
echo.
streamlit run app\Home.py
pause
