from .models import Lead

INDUSTRY_FIT = {'SaaS', 'FinTech', 'HealthTech', 'EdTech', 'Logistics', 'Cybersecurity', 'HRTech'}
JOB_FIT_WORDS = ('HR', 'People', 'Operations', 'Revenue', 'Sales', 'Founder', 'CEO', 'COO')




def score_breakdown_for_lead(lead):
    return {
        'industry_fit': 25 if lead.industry in INDUSTRY_FIT else 10,
        'company_size_fit': 20 if lead.company_size in {'51-200', '201-500', '501-1000'} else 10,
        'job_title_fit': 20 if any(w.lower() in lead.job_title.lower() for w in JOB_FIT_WORDS) else 8,
        'growth_signal': 25 if (lead.company_growth or lead.hiring_signal or lead.leadership_change) else 5,
        'contact_availability': 10 if lead.contact_available and lead.email else 0,
    }


def calculate_lead_score(lead: Lead):
    industry = 25 if lead.industry in INDUSTRY_FIT else 10
    size = 20 if lead.company_size in {'51-200', '201-500', '501-1000'} else 10
    title = 20 if any(w.lower() in lead.job_title.lower() for w in JOB_FIT_WORDS) else 8
    growth = 25 if (lead.company_growth or lead.hiring_signal or lead.leadership_change) else 5
    contact = 10 if lead.contact_available and lead.email else 0
    total = min(100, industry + size + title + growth + contact)
    priority = 'high' if total >= 75 else 'medium' if total >= 45 else 'low'

    reasons = {
        'industry_fit': industry,
        'company_size_fit': size,
        'job_title_fit': title,
        'growth_signal': growth,
        'contact_availability': contact,
    }

    signal = lead.signal_description or 'No additional signal recorded.'
    if lead.hiring_signal:
        why = f'{lead.company} has a recorded hiring signal: {signal}'
        action = 'Reference the hiring trigger and propose a short discovery call.'
        angle = 'Hiring/growth creates an opportunity to discuss onboarding and sales productivity.'
    elif lead.company_growth:
        why = f'{lead.company} has a recorded growth signal: {signal}'
        action = 'Use the growth signal as the opening context for outreach.'
        angle = 'Tie the message to scaling challenges and repeatable sales execution.'
    elif lead.leadership_change:
        why = f'{lead.company} has a recorded leadership-change signal: {signal}'
        action = 'Acknowledge the recorded leadership change and offer a concise value discussion.'
        angle = 'Position the product as a way to accelerate sales execution during transition.'
    else:
        why = f'{lead.company} matches some ICP fields, but no strong growth trigger is recorded.'
        action = 'Use a relevance-first message and ask one discovery question.'
        angle = 'Lead with the strongest verified ICP fit and avoid unsupported claims.'

    lead.score = total
    lead.priority = priority
    lead.why_now = why
    lead.recommended_action = action
    lead.message_angle = angle
    lead.save(update_fields=['score','priority','why_now','recommended_action','message_angle','updated_at'])
    return {'total': total, 'priority': priority, 'breakdown': reasons}
