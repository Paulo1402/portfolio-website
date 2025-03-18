from django.db import models

from app.models.base import BaseModel


class Skill(BaseModel):
    name = models.CharField(max_length=30)
    area = models.ForeignKey("SkillArea", on_delete=models.CASCADE)
    show = models.BooleanField(default=True)

    def __str__(self):
        return self.name
