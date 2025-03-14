from django.db import models


class Profile(models.Model):
    description = models.TextField()
    email = models.EmailField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    github = models.URLField(null=True, blank=True)
    picture = models.ImageField(upload_to="profile/", null=True, blank=True)

    class Meta:
        verbose_name_plural = "Profile"

    def __str__(self):
        return "Profile"

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
