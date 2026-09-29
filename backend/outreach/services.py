import os
import requests
from .models import OutreachDraft

def fallback_draft(lead, tone):
    greeting = f'Hi {lead.name.split()[0]},'
    tone_line = {
        'professional': 'I am reaching out with a focused idea for your sales workflow.',
        'friendly': 'I wanted to share a quick idea that may be useful for your team.',
        'concise': 'A quick idea for your sales workflow.',
    }.get(tone, 'I am reaching out with a focused idea for your sales workflow.')
    return {
        'subject': f'{lead.company}: a timely sales execution idea',
        'body': f'{greeting}\n\n{tone_line} {lead.why_now}\n\n{lead.message_angle}\n\nWould it be useful to compare notes for 15 minutes?\n\nBest,\nSignalFlow AI',
        'cta': 'Would a 15-minute conversation be useful?',
        'source': 'fallback',
        'disclaimer': 'Fallback draft — no AI API key configured.',
    }

def generate_outreach_draft(user, lead, tone):
    key = os.getenv('OPENAI_API_KEY')
    if not key:
        data = fallback_draft(lead, tone)
        OutreachDraft.objects.create(user=user, lead=lead, tone=tone, subject=data['subject'], body=data['body'], cta=data['cta'], source='fallback')
        return data
    prompt = (f"Create a sales outreach draft using ONLY the facts below. Do not invent details, relationships, customers, metrics, or events.\n"
              f"Lead: {lead.name}\nCompany: {lead.company}\nJob title: {lead.job_title}\nIndustry: {lead.industry}\nCompany size: {lead.company_size}\n"
              f"Verified/sample signal: {lead.signal_description}\nWhy Now: {lead.why_now}\nMessage angle: {lead.message_angle}\nTone: {tone}\n"
              "Return strict JSON with keys subject, body, cta.")
    try:
        resp = requests.post('https://api.openai.com/v1/chat/completions', headers={'Authorization': f'Bearer {key}','Content-Type':'application/json'}, json={'model': os.getenv('OPENAI_MODEL','gpt-4o-mini'),'temperature':0.3,'response_format':{'type':'json_object'},'messages':[{'role':'system','content':'You write concise B2B outreach copy from supplied facts only.'},{'role':'user','content':prompt}]}, timeout=30)
        resp.raise_for_status()
        data = resp.json()['choices'][0]['message']['content']
        import json
        obj = json.loads(data)
        result = {'subject': obj['subject'], 'body': obj['body'], 'cta': obj['cta'], 'source':'openai', 'disclaimer':'AI draft — review before sending.'}
        OutreachDraft.objects.create(user=user, lead=lead, tone=tone, subject=result['subject'], body=result['body'], cta=result['cta'], source='openai')
        return result
    except Exception:
        data = fallback_draft(lead, tone)
        data['disclaimer'] = 'AI service unavailable — deterministic fallback draft used.'
        OutreachDraft.objects.create(user=user, lead=lead, tone=tone, subject=data['subject'], body=data['body'], cta=data['cta'], source='fallback')
        return data
