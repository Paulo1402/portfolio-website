from django.contrib import admin

from app.models import Skill


class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "area", "show", "created_at", "updated_at")


admin.site.register(Skill, SkillAdmin)
