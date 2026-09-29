from django.contrib import admin
from .models import Lead
@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('name','company','job_title','industry','score','priority','status','owner')
    list_filter = ('industry','company_size','status','priority','signal_type')
    search_fields = ('name','email','company','job_title')
