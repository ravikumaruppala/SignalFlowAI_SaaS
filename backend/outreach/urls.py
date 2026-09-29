from django.urls import path
from .views import latest_drafts_view, save_draft_view, send_lead_email_view
urlpatterns = [path('drafts/', latest_drafts_view), path('drafts/save/', save_draft_view), path('send/', send_lead_email_view)]
