from django.contrib import admin

from app.models import Skill


class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "area", "show")


admin.site.register(Skill, SkillAdmin)
