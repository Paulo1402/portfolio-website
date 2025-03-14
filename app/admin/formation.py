import tagulous.admin
from django.contrib import admin

from app.models import Formation
from app.forms.base import BaseStartDateEndDateForm


class FormationAdminForm(BaseStartDateEndDateForm):
    class Meta:
        model = Formation
        fields = "__all__"


class FormationAdmin(admin.ModelAdmin):
    form = FormationAdminForm
    fieldsets = (
        ("Certification Information", {"fields": ("title", "institution")}),
        ("Duration", {"fields": ("start_date", "end_date")}),
        ("Details", {"fields": ("description", "topics")}),
    )


tagulous.admin.register(Formation, FormationAdmin)
