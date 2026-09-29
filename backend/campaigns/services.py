from .models import SequenceStep

def ensure_default_sequence(campaign):
    defaults = [
        (1, 1, 'Kickoff outreach', 'Hi {{name}},\n\nI noticed {{company}} has a recent signal relevant to sales execution. {{message_angle}}\n\nWould a 15-minute conversation be useful?'),
        (2, 3, 'Quick follow-up', 'Hi {{name}},\n\nFollowing up on my note. I can share a concise example of how teams use SignalFlow AI to prioritize the next sales action.\n\nOpen to a quick chat?'),
        (3, 6, 'Closing the loop', 'Hi {{name}},\n\nI will close the loop for now. If improving lead prioritization or timely outreach becomes a priority at {{company}}, I would be happy to reconnect.\n\nBest,'),
    ]
    for n, day, subject, body in defaults:
        SequenceStep.objects.get_or_create(campaign=campaign, step_number=n, defaults={
            'day_offset': day, 'channel': 'email', 'subject_template': subject, 'body_template': body
        })
