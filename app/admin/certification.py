import tagulous.admin
from django.contrib import admin

from app.models import Certification
from app.forms.base import BaseStartDateEndDateForm


class CertificationAdminForm(BaseStartDateEndDateForm):
    class Meta:
        model = Certification
        fields = "__all__"
        exclude = ("created_at", "updated_at")


class CertificationAdmin(admin.ModelAdmin):
    form = CertificationAdminForm
    fieldsets = (
        ("Certification Information", {"fields": ("title", "institution")}),
        ("Duration", {"fields": ("start_date", "end_date")}),
        ("Details", {"fields": ("description", "url", "topics")}),
    )
    list_display = ("title", "institution", "created_at", "updated_at")


tagulous.admin.register(Certification, CertificationAdmin)
