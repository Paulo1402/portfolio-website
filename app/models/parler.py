from django.db import models

from parler.models import TranslatableModel, TranslatedFields


class News(TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField(max_length=255),
        text=models.TextField(),
    )

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]

    # def __str__(self):
    #     return self.title
