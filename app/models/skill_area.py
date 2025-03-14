from django.db import models


class SkillArea(models.Model):
    name = models.CharField(max_length=30)
    index = models.IntegerField(blank=True, null=True)
    show = models.BooleanField(default=True)

    def __str__(self):
        return self.name
