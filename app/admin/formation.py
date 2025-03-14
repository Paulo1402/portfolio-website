import tagulous.admin
from django.contrib import admin

from app.models import Formation


class FormationAdmin(admin.ModelAdmin):
    pass


tagulous.admin.register(Formation, FormationAdmin)
