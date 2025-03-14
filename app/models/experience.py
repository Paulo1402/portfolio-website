import tagulous.models
from django.db import models

from app.models.base import BaseStartDateEndDateModel
from app.models.topic import Topic


class Experience(BaseStartDateEndDateModel):
    title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    description = models.TextField()
    topics = tagulous.models.TagField(Topic, blank=True)

    def __str__(self):
        return self.title
