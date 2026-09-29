# API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/auth/csrf/` | Set CSRF cookie |
| POST | `/api/auth/register/` | Register user |
| POST | `/api/auth/login/` | Authenticate |
| POST | `/api/auth/logout/` | Logout |
| GET | `/api/auth/me/` | Current user |
| PATCH | `/api/auth/profile/` | Update profile |
| GET/POST | `/api/leads/` | List/filter/create leads |
| GET/PATCH/DELETE | `/api/leads/{id}/` | Lead CRUD |
| POST | `/api/leads/{id}/score/` | Recalculate score |
| POST | `/api/leads/{id}/generate-email/` | Generate outreach draft |
| GET/POST | `/api/campaigns/` | List/create campaigns |
| GET/PATCH/DELETE | `/api/campaigns/{id}/` | Campaign CRUD |
| POST | `/api/campaigns/{id}/leads/` | Assign leads |
| POST | `/api/campaigns/{id}/simulate/` | Simulate send/open/reply/meeting |
| GET/POST | `/api/sequences/` | Sequence steps |
| GET | `/api/inbox/` | Simulated replies |
| PATCH | `/api/inbox/{id}/` | Reply category/status |
| GET | `/api/analytics/` | Aggregated metrics |
| GET | `/api/dashboard/` | Dashboard metrics + recent activity |

## Payment endpoints

- `POST /api/payments/create-order/` — server-side Razorpay order creation for a paid plan.
- `POST /api/payments/verify/` — verify the Razorpay checkout signature and activate the plan.
- `GET /api/payments/subscription/` — return the current user's active plan or Free plan.
- `GET /api/payments/history/` — return recent payment records for the current user.


## Password reset

- `POST /api/auth/password/request-otp/` — send a 6-digit password-reset OTP by email.
- `POST /api/auth/password/reset/` — verify OTP and set the new password.

## Real lead email

- `POST /api/outreach/send/` — send the reviewed draft to the lead through the configured Gmail SMTP account and record an `email_sent` activity.
