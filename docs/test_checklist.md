# Manual E2E Test Checklist

- [ ] Register a new user.
- [ ] Login and verify dashboard.
- [ ] Logout and verify protected routes redirect.
- [ ] Lead search works.
- [ ] Filter by industry, size, title, status, score and signal.
- [ ] Create a lead.
- [ ] Edit a lead.
- [ ] Delete a lead.
- [ ] Recalculate score and verify component totals = 100 maximum.
- [ ] Open Why Now and verify evidence comes from stored fields.
- [ ] Generate fallback email without an AI key.
- [ ] Edit and save an outreach draft.
- [ ] Create a campaign.
- [ ] Assign the same lead twice and verify duplicate prevention.
- [ ] View Day 1/3/6 sequence.
- [ ] Simulate send/open/reply/meeting.
- [ ] Open Inbox and update reply category.
- [ ] Verify lead status changes after a reply.
- [ ] Refresh Analytics and verify totals change only after persisted simulation events.
- [ ] Verify sales rep cannot access another user's records.
- [ ] Verify manager sees team aggregates.
- [ ] Verify staff can use Django Admin.

# New feature checks
- [ ] Landing page is public at `/`.
- [ ] Landing-page Login button opens `/login` when logged out.
- [ ] Landing-page Login button opens `/dashboard` when already authenticated.
- [ ] Remember Me creates a persistent 30-day Django session.
- [ ] Without Remember Me, closing the browser removes the session cookie.
- [ ] Forgot password sends a 6-digit OTP by Gmail SMTP.
- [ ] OTP expires after 10 minutes and is limited to 5 attempts.
- [ ] Correct OTP changes the account password.
- [ ] Lead detail can send a reviewed draft to the lead through Gmail SMTP.
- [ ] Real `email_sent` activity appears in the activity timeline and send analytics.
