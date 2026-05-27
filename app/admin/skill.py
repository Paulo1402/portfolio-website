from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from app.models import Skill


class SkillAdmin(TranslationAdmin):
    list_display = ("name", "area", "show", "created_at", "updated_at")


admin.site.register(Skill, SkillAdmin)
