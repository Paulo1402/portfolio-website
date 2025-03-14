from django.contrib import admin
from django import forms

import tagulous.admin
from app.models import Certification
from app.forms.widgets import MonthYearWidget, MonthYearField


class ClassificationAdminForm(forms.ModelForm):
    start_date = MonthYearField(widget=MonthYearWidget(format="%Y-%m"), required=False)
    end_date = MonthYearField(widget=MonthYearWidget(format="%Y-%m"), required=False)

    class Meta:
        model = Certification
        fields = "__all__"


class CertificationAdmin(admin.ModelAdmin):
    form = ClassificationAdminForm
    fieldsets = (
        ("Certification Information", {"fields": ("title", "institution")}),
        ("Duration", {"fields": ("start_date", "end_date")}),
        ("Details", {"fields": ("description", "url", "topics")}),
    )


tagulous.admin.register(Certification, CertificationAdmin)
