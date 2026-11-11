@echo off
REM Gera dist\RetiradaSenha.exe (rodar no Windows, dentro da pasta do projeto)
if not exist .env (
  echo Crie o arquivo .env a partir do .env.example
  pause
  exit /b 1
)
python -m pip install -r requirements.txt
python -m PyInstaller --onefile --console --name RetiradaSenha --add-data ".env;." app.py
echo.
echo Pronto: dist\RetiradaSenha.exe
pause
