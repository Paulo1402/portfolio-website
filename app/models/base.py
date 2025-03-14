from django.db import models


class BaseStartDateEndDateModel(models.Model):
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    class Meta:
        abstract = True
