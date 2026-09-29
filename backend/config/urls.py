from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/leads/', include('leads.urls')),
    path('api/campaigns/', include('campaigns.urls')),
    path('api/outreach/', include('outreach.urls')),
    path('api/sequences/', include('campaigns.sequence_urls')),
    path('api/inbox/', include('inbox.urls')),
    path('api/analytics/', include('analytics_app.urls')),
    path('api/dashboard/', include('analytics_app.dashboard_urls')),
    path('api/payments/', include('payments.urls')),
]
