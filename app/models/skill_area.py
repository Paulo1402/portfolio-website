from django.db import models

from app.models.base import BaseModel


class SkillArea(BaseModel):
    name = models.CharField(max_length=30)
    index = models.IntegerField(blank=True, null=True)
    show = models.BooleanField(default=True)

    def __str__(self):
        return self.name
