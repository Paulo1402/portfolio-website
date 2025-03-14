import tagulous.models
from django.db import models

from app.models.base import BaseStartDateEndDateModel
from app.models.topic import Topic


class Certification(BaseStartDateEndDateModel):
    title = models.CharField(max_length=100)
    institution = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    topics = tagulous.models.TagField(Topic, blank=True)

    def __str__(self):
        return self.title
