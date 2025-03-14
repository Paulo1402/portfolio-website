import tagulous.admin
from django.contrib import admin

from app.models import Experience


class ExperienceAdmin(admin.ModelAdmin):
    pass


tagulous.admin.register(Experience, ExperienceAdmin)
