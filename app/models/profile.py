from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from app.models.base import BaseModel


class Profile(BaseModel):
    description = models.TextField()
    email = models.EmailField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    github = models.URLField(null=True, blank=True)
    picture = models.ImageField(upload_to="profile/", null=True, blank=True)

    class Meta:
        verbose_name_plural = "Profile"

    def __str__(self):
        return "Profile"

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def clean(self):
        super().clean()

        if Profile.objects.exclude(pk=self.pk).exists():
            raise ValidationError(_("Only one profile can exist."))

    @property
    def linkedin_username(self):
        return self._get_username_from_url(self.linkedin)

    @property
    def github_username(self):
        return self._get_username_from_url(self.github)

    @staticmethod
    def _get_username_from_url(user_url):
        if not user_url:
            return ""

        if user_url.endswith("/"):
            user_url = user_url[:-1]

        return user_url.split("/")[-1]
