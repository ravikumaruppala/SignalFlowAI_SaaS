# Architecture

```text
React (5173)
   |
   | Axios + session cookie + CSRF header
   v
Django REST Framework (8000)
   |\
   | \-- services.py -> scoring / Why Now / AI draft / payments
   |
   v
MySQL 8
```

## Request flow
1. React loads and requests `/api/auth/csrf/`.
2. User logs in using session authentication.
3. Browser keeps the HttpOnly session cookie.
4. React sends the CSRF token from the `csrftoken` cookie on mutating requests.
5. Django permissions enforce ownership/team access.
6. Business rules stay in backend services.
7. Analytics are derived from persisted `Activity` and `Lead` records.

## Deliberate MVP constraints
- Sample/imported signal data; no live scraping.
- Three fixed sequence steps: Day 1, Day 3, Day 6.
- Simulated outbound events.
- Razorpay test-mode one-time plan checkout; recurring auto-renewal is future scope.
- No real HubSpot sync.

## Payment flow

```text
React Plans
   ↓
POST /api/payments/create-order/
   ↓
Django → Razorpay Orders API
   ↓
Razorpay Standard Checkout
   ↓
React success handler
   ↓
POST /api/payments/verify/
   ↓
Django verifies HMAC signature + provider order/amount
   ↓
Payment + Subscription stored in MySQL
```
