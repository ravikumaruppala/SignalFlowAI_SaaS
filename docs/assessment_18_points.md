# BusinessLabs 18-Point Assessment Mapping

1. **Product concept** — SignalFlow AI turns a lead list into a reason-to-contact, message, sequence and measurable result.
2. **2-day MVP scope** — Core domain only; no live scraping/sending dependency. Razorpay test-mode checkout is included for the payment requirement.
3. **Competitor research** — HubSpot, Instantly, Apollo, Clay and Gong are conceptual references.
4. **Differentiator** — Explainable “Why Now?” decision aid.
5. **MVP features** — Authentication, leads, scoring, Why Now, AI outreach, campaigns, sequence, analytics, inbox and admin.
6. **Roles** — Sales Rep, Sales Manager, Admin.
7. **Journey** — Dashboard → Leads → Lead detail → Outreach → Campaign → Sequence → Inbox → Analytics → Profile.
8. **Database** — User, Lead, Campaign, SequenceStep, CampaignLead, Activity plus drafts/replies.
9. **Architecture** — React + DRF + MySQL, with AI called from Django.
10. **Django structure** — Modular apps and services layer.
11. **API** — REST endpoints for auth, leads, campaigns, sequences, inbox, dashboard and analytics.
12. **2-day plan** — Setup/auth → leads/score → outreach/campaigns → inbox/analytics/admin/test.
13. **5 slides** — Problem, solution/workflow, TAM/SAM/SOM, business model, competition/roadmap.
14. **Business model** — Free, Starter, Professional, Business; illustrative only.
15. **TAM/SAM/SOM** — Use the figures in the supplied blueprint; clearly label research vs internal assumptions.
16. **Demo** — Login, dashboard, filters, high-score lead, Why Now, AI outreach, campaign, sequence, analytics, inbox/admin.
17. **Interview material** — Explain stack choices, scoring, AI safety, scaling and future integrations.
18. **Roadmap** — Recurring billing, CRM sync, calendar, enrichment, richer signals, multichannel, team controls. User-triggered Gmail SMTP email sending is now implemented; automated multistep delivery remains future scope.

## Assessment instruction fit
The supplied instruction image asks the team to study competitors, define marketplace features, plan data/models, ensure role-specific logged-in experiences, provide filters, plan admin control, build the core locally, consider payments and CRM API integration, and cover TAM/SAM/SOM and the revenue model. Those ideas are reflected here as working MVP features or explicitly labeled future scope; Razorpay checkout is implemented in test mode for the payment requirement.

## Frontend architecture override
The supplied blueprint originally described Django templates + Bootstrap. For this implementation, the frontend is intentionally implemented as React.js + Vite + Tailwind CSS while Django REST Framework remains the backend API and MySQL remains the database.
