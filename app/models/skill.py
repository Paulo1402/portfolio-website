from django.db import models


class Skill(models.Model):
    name = models.CharField(max_length=30)
    show = models.BooleanField(default=True)
    area = models.ForeignKey("SkillArea", on_delete=models.CASCADE)

    def __str__(self):
        return self.name
