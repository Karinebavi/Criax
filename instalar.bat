@echo off
REM Instalador do Esteira LIE (Windows).
REM Cria o ambiente virtual .venv e instala as dependencias.

cd /d "%~dp0"

echo ==============================================
echo   Instalando o Esteira LIE
echo ==============================================

REM Procura o Python.
where python >nul 2>nul
if %errorlevel%==0 (
  set PY=python
) else (
  where py >nul 2>nul
  if %errorlevel%==0 (
    set PY=py
  ) else (
    echo ERRO: Python nao foi encontrado.
    echo Instale o Python 3.11 ou superior em https://www.python.org/downloads/ e rode de novo.
    echo IMPORTANTE: marque a opcao "Add Python to PATH" durante a instalacao.
    pause
    exit /b 1
  )
)

%PY% --version

REM Cria o ambiente virtual se ainda nao existir.
if not exist ".venv" (
  echo Criando ambiente virtual (.venv)...
  %PY% -m venv .venv
)

REM Ativa e instala tudo.
call .venv\Scripts\activate.bat
echo Atualizando o pip...
python -m pip install --upgrade pip
echo Instalando as dependencias (pode demorar alguns minutos)...
python -m pip install -r requirements.txt

echo.
echo ==============================================
echo   Pronto! Instalacao concluida.
echo   Agora rode:  rodar.bat
echo ==============================================
pause
