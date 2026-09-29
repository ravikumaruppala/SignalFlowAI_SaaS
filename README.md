# SignalFlow AI — BusinessLabs Marketing SaaS MVP

A two-day-assessment-friendly sales execution MVP based on the supplied BusinessLabs brief.

**Core workflow:** Lead → Signal → Reason → Message → Sequence → Result

## Stack
- Frontend: React.js + JavaScript + Vite + React Router + Axios + Tailwind CSS + lucide-react + Recharts
- Backend: Python 3.12+ + Django + Django REST Framework + django-cors-headers
- Database: MySQL 8
- Authentication: Django session authentication + CSRF protection
- Payments: Razorpay Standard Checkout in test mode with server-side order creation and signature verification
- Email: Gmail SMTP for password-reset OTPs and user-triggered real lead emails (Google App Password)
- AI: optional OpenAI API from Django; deterministic fallback when no API key is configured

## MVP scope
The application implements the assessment's core workflow: authentication, role-aware access, lead CRUD/search/filtering, explainable lead scoring, Why Now signals, AI-assisted outreach with fallback, campaigns, fixed Day 1/3/6 sequences, simulated opens/replies/meetings, real user-triggered email sends, analytics, illustrative subscription plans, and Django Admin.

Live scraping/enrichment, LinkedIn/WhatsApp automation, recurring auto-renewal, and real HubSpot synchronization remain future scope. Gmail SMTP email sending, password-reset OTP, and Razorpay one-time plan checkout are implemented.

## Project structure
```text
SignalFlow_AI_MVP/
  backend/
    manage.py
    requirements.txt
    .env.example
    config/
    accounts/
    leads/
    campaigns/
    outreach/
    inbox/
    analytics_app/
    payments/
  frontend/
    package.json
    .env.example
    index.html
    src/
  docs/
```

## Windows + VS Code setup

### 1. Prerequisites
Install:
- Python 3.12+ (Python 3.13 is supported by this code)
- Node.js 20+
- MySQL 8
- VS Code

### 2. Start/check MySQL
In PowerShell:
```powershell
Get-Service MySQL* | Select-Object Name,Status
```
If your MySQL service is named `MySQL80`:
```powershell
Start-Service MySQL80
```
If it uses a different name, start that service from `services.msc`.

### 3. Create database
Open MySQL client / MySQL Workbench and run:
```sql
CREATE DATABASE signalflow_ai CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'signalflow'@'localhost' IDENTIFIED BY 'SignalFlow@123';
GRANT ALL PRIVILEGES ON signalflow_ai.* TO 'signalflow'@'localhost';
FLUSH PRIVILEGES;
```

### 4. Open the project
```powershell
cd SignalFlow_AI_MVP
code .
```

### 5. Backend terminal
```powershell
cd backend
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```
Edit `backend\.env` and set your MySQL credentials. The provided values match the sample SQL above.

Then:
```powershell
python manage.py makemigrations accounts leads campaigns outreach inbox payments
python manage.py migrate
python manage.py seed_demo
python manage.py runserver 8000
```

### 6. Frontend terminal
Open a second PowerShell terminal:
```powershell
cd SignalFlow_AI_MVP\frontend
npm install
npm run dev
```
Open:
`http://localhost:5173`

### 7. Demo credentials
Seed command creates:
- Sales Rep: `sales@signalflow.local` / `Demo@12345`
- Manager: `manager@signalflow.local` / `Demo@12345`
- Admin: `admin@signalflow.local` / `Admin@12345`

These are local demo credentials only. Change them outside local assessment use.

### 8. Django Admin
Open:
`http://localhost:8000/admin/`

## Razorpay payment gateway

The Plans page now supports **Razorpay Standard Checkout in test mode** for Starter and Professional. The backend creates the Razorpay order and verifies the returned checkout signature before activating a 30-day plan. Razorpay documents that every payment should have a server-created order and that the successful checkout response should be verified server-side. citeturn658330search0turn658330search1

### 1. Create Razorpay test credentials
Create a Razorpay account and use **test-mode** API credentials for local development. Put them only in `backend/.env`:
```env
RAZORPAY_KEY_ID=rzp_test_your_key_id
RAZORPAY_KEY_SECRET=your_test_key_secret
RAZORPAY_CURRENCY=INR
```

### 2. Start the project
Use the normal backend and frontend commands above. Open:
`http://localhost:5173/plans`

### 3. Test a payment
Click **Pay with Razorpay** on Starter or Professional. The frontend requests an order from Django, opens Razorpay Checkout, then sends the payment ID, order ID and signature back to Django for verification. The application stores the transaction and activates the selected plan for 30 days.

### 4. Important security rules
- Never put `RAZORPAY_KEY_SECRET` in React or commit it to Git.
- The amount is determined by Django, not by a client-supplied price.
- The signature is verified with the server-side secret.
- The project stores provider IDs and status in MySQL.
- Real recurring subscriptions can be added later with Razorpay Subscriptions and webhooks. Razorpay provides subscription APIs and webhook notifications for recurring billing. citeturn909729search0

## Gmail SMTP email sending

The MVP now supports two real email workflows: password-reset OTPs and user-triggered emails to leads. Both use Django SMTP with Gmail. Google states that App Passwords require 2-Step Verification; use an App Password rather than your normal Gmail password. citeturn493275search0turn493275search8

Add these values to `backend/.env`:
```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
EMAIL_HOST_USER=yourgmail@gmail.com
EMAIL_HOST_PASSWORD=your_16_digit_app_password
DEFAULT_FROM_EMAIL=yourgmail@gmail.com
EMAIL_TIMEOUT=20
```

The SMTP secret stays on the Django server and is not sent to React.

### Google App Password setup
1. Enable 2-Step Verification on the Google account used to send mail.
2. Open the Google Account security settings and create an App Password.
3. Copy the generated 16-character App Password and put it in `EMAIL_HOST_PASSWORD` (without spaces).
4. Restart Django after saving `.env`.

The app uses Gmail SMTP for both the OTP email and the real lead email.

## Optional AI
The MVP works without an external AI key. To use OpenAI, set in `backend/.env`:
```env
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4o-mini
```
Generated copy is always reviewed/edited in the UI and is never automatically sent.

## API and security notes
- Frontend uses Axios with `withCredentials=true`.
- React requests `/api/auth/csrf/` before POST/PATCH/DELETE actions.
- CSRF and CORS are configured for `http://localhost:5173`.
- API keys stay server-side in Django.
- Object permissions prevent sales reps from accessing unrelated records.
- Passwords use Django's password hashing.

## Common Windows fixes

### MySQL access denied
Confirm `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, and `DB_PORT` in `.env`, then test the credentials in MySQL Workbench.

### CORS/CSRF error
Ensure the frontend is running on `http://localhost:5173` and `FRONTEND_URL=http://localhost:5173` exists in `backend/.env`.

### `mysqlclient` build problems
This project uses PyMySQL to avoid native build steps on Windows.

### Node package issue
```powershell
node -v
npm -v
npm install
```
Use Node.js 20+.

### Port already used
```powershell
python manage.py runserver 8001
npm run dev -- --port 5174
```
Update `.env` values if you change ports.

## Testing
Backend unit/integration tests:
```powershell
cd backend
python manage.py test
```

Manual checklist is in `docs/test_checklist.md`.

## What is real vs simulated
**Real:** MySQL persistence, authentication, authorization, lead CRUD/filtering, deterministic scoring, Why Now reasoning, campaign/sequence persistence, inbox status updates, analytics aggregation, Django Admin.

**Optional:** OpenAI generation, only when an API key is configured.

**Simulated:** opens/replies/meetings and inbox responses. **Real:** user-triggered Gmail SMTP email sends and password-reset OTP emails when EMAIL_HOST_USER/EMAIL_HOST_PASSWORD are configured.

## Assessment documents
See `docs/` for the 18-point mapping, architecture, API list, database notes, 5-slide presentation, demo script, and test checklist.
