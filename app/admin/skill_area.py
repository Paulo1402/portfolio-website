from django.contrib import admin

from app.models import SkillArea


class SkillAreaAdmin(admin.ModelAdmin):
    list_display = ("name", "index", "show", "created_at", "updated_at")


admin.site.register(SkillArea, SkillAreaAdmin)
