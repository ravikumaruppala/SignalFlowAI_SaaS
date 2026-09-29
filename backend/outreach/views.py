from django.core.mail import EmailMessage
from django.db import transaction
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from inbox.models import Activity
from leads.models import Lead
from .models import OutreachDraft
from .serializers import OutreachDraftSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def latest_drafts_view(request):
    return Response(OutreachDraftSerializer(OutreachDraft.objects.filter(user=request.user)[:20], many=True).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_draft_view(request):
    data = request.data.copy()
    lead_id = data.get('lead')
    if not Lead.objects.filter(id=lead_id, owner__team_name=request.user.team_name).exists():
        return Response({'detail': 'Lead is not accessible.'}, status=403)
    data['user'] = request.user.id
    ser = OutreachDraftSerializer(data=data)
    ser.is_valid(raise_exception=True)
    obj = ser.save(user=request.user, source=data.get('source', 'manual'))
    return Response(OutreachDraftSerializer(obj).data, status=201)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_lead_email_view(request):
    """Send a user-reviewed draft to the selected lead via the configured Gmail SMTP account."""
    lead_id = request.data.get('lead')
    subject = str(request.data.get('subject', '')).strip()
    body = str(request.data.get('body', '')).strip()
    cta = str(request.data.get('cta', '')).strip()

    if not subject or not body:
        return Response({'detail': 'Subject and email body are required.'}, status=400)

    lead = Lead.objects.filter(id=lead_id).select_related('owner').first()
    if not lead:
        return Response({'detail': 'Lead not found.'}, status=404)

    if request.user.role == 'sales_rep' and lead.owner_id != request.user.id:
        return Response({'detail': 'You cannot email this lead.'}, status=403)
    if request.user.role != 'sales_rep' and lead.owner.team_name != request.user.team_name:
        return Response({'detail': 'You cannot email this lead.'}, status=403)
    if not lead.email:
        return Response({'detail': 'This lead has no email address.'}, status=400)

    content = body
    if cta and cta not in body:
        content = f'{body}\n\n{cta}'

    try:
        message = EmailMessage(
            subject=subject,
            body=content,
            from_email=None,
            to=[lead.email],
            reply_to=[request.user.email] if request.user.email else None,
        )
        sent = message.send(fail_silently=False)
    except Exception as exc:
        return Response(
            {'detail': f'Unable to send email. Check Gmail SMTP settings in backend/.env. ({exc})'},
            status=503,
        )

    if sent != 1:
        return Response({'detail': 'Email was not accepted by the configured SMTP server.'}, status=503)

    with transaction.atomic():
        draft = OutreachDraft.objects.create(
            user=request.user,
            lead=lead,
            tone=str(request.data.get('tone', 'professional')),
            subject=subject,
            body=body,
            cta=cta or 'Email sent',
            source='sent_gmail',
        )
        Activity.objects.create(
            user=request.user,
            lead=lead,
            campaign=None,
            activity_type='email_sent',
            metadata={
                'real': True,
                'provider': 'gmail_smtp',
                'recipient': lead.email,
                'subject': subject,
                'draft_id': draft.id,
            },
        )
        lead.status = 'contacted'
        lead.save(update_fields=['status', 'updated_at'])

    return Response({
        'detail': f'Email sent to {lead.email}.',
        'recipient': lead.email,
        'draft_id': draft.id,
    })
