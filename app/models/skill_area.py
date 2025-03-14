from django.db import models


class SkillArea(models.Model):
    name = models.CharField(max_length=30)
    show = models.BooleanField(default=True)
    index = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name
