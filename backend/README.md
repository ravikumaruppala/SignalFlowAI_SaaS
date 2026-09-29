# SignalFlow AI Backend

Run from this directory:
```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python manage.py makemigrations
python manage.py migrate
python manage.py seed_demo
python manage.py runserver 8000
```
