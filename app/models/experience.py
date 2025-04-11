import tagulous.models
from django.db import models
from parler.models import TranslatableModel, TranslatedFields

from app.models.base import BaseStartDateEndDateModel
from app.models.topic import Topic


class Experience(TranslatableModel, BaseStartDateEndDateModel):
    translations = TranslatedFields(
        title=models.CharField(max_length=100),
        company=models.CharField(max_length=100),
        description=models.TextField(),
    )

    topics = tagulous.models.TagField(Topic, blank=True)

    def __str__(self):
        return self.title
