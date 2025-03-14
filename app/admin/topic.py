import tagulous.admin
from django.contrib import admin

from app.models import Topic


class TopicAdmin(tagulous.admin.TagModelAdmin):
    pass


admin.site.register(Topic, TopicAdmin)
