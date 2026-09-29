Set-Location "$PSScriptRoot\backend"
if (!(Test-Path .venv)) { py -3 -m venv .venv }
.\.venv\Scripts\Activate.ps1
python manage.py runserver 8000
