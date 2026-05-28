from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from app.models import SkillArea


class SkillAreaAdmin(TranslationAdmin):
    list_display = ("name", "index", "show", "created_at", "updated_at")


admin.site.register(SkillArea, SkillAreaAdmin)
