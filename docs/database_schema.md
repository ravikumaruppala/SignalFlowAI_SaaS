# Database Schema

## Tables
- `accounts_user`: Django custom user, email login, role.
- `leads_lead`: owner, contact/company fields, score, signal and explanation fields.
- `campaigns_campaign`: campaign metadata and owner.
- `campaigns_sequencestep`: Day 1/3/6 sequence templates.
- `campaigns_campaignlead`: many-to-many campaign/lead bridge with unique pair.
- `outreach_outreachdraft`: generated draft copy and tone/source metadata.
- `inbox_inboxreply`: simulated inbound replies.
- `inbox_activity`: timeline and analytics event store.

## Main relationships
- User 1→N Lead
- User 1→N Campaign
- Campaign 1→N SequenceStep
- Campaign N↔N Lead through CampaignLead
- Lead 1→N Activity
- Lead 1→N InboxReply

## Payment tables

The payment-enabled version adds two application tables:

### Payment
- `id` — primary key
- `user_id` — FK to `accounts.User`
- `plan_code` — Starter or Professional
- `amount` — amount in paise
- `currency` — INR
- `razorpay_order_id` — unique provider order ID
- `razorpay_payment_id` — provider payment ID after checkout
- `razorpay_signature` — signature returned by Checkout
- `status` — created / verified / failed / refunded
- `provider_status` — provider status returned by Razorpay
- timestamps

### Subscription
- `id` — primary key
- `user_id` — FK to `accounts.User`
- `plan_code` — Free / Starter / Professional / Business
- `status` — active / expired / cancelled
- `starts_at`
- `ends_at`
- `source_payment_id` — optional FK to Payment
- timestamps

Payment flow:
`React Plans → Django create-order → Razorpay Checkout → React success handler → Django verify signature → Payment row → Subscription row`
