from django.db import models


class Skill(models.Model):
    name = models.CharField(max_length=30)
    area = models.ForeignKey("SkillArea", on_delete=models.CASCADE)
    show = models.BooleanField(default=True)

    def __str__(self):
        return self.name
