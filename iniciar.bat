@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo === ENIGMA: iniciando ===
call conda activate escaperoomapp
if errorlevel 1 (echo Nao achei o conda. Abra pelo terminal do VSCode ou pelo Anaconda Prompt. & pause & exit /b 1)
pip install -r requirements.txt
if not exist .env (echo Crie o arquivo .env antes. Veja o README.md. & pause & exit /b 1)
python manage.py makemigrations
python manage.py migrate
start http://localhost:8000
python manage.py runserver
pause
