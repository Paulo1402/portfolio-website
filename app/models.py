import os

import tagulous.models
from django.db import models
from django.utils.text import slugify


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


class Skill(models.Model):
    name = models.CharField(max_length=30)
    show = models.BooleanField(default=True)
    area = models.ForeignKey("SkillArea", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class SkillArea(models.Model):
    name = models.CharField(max_length=30)
    show = models.BooleanField(default=True)
    index = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name


class Topic(tagulous.models.TagModel):
    class TagMeta:
        autocomplete_view = "topic_autocomplete"
        force_lowercase = True


class BaseStartDateEndDateModel(models.Model):
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    class Meta:
        abstract = True

    def formated_start_date(self):
        return self.start_date.strftime("%B %Y")

    def formated_end_date(self):
        return self.end_date.strftime("%B %Y")


class Experience(BaseStartDateEndDateModel):
    title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    description = models.TextField()
    topics = tagulous.models.TagField(Topic, blank=True)

    def __str__(self):
        return self.title


class Formation(BaseStartDateEndDateModel):
    title = models.CharField(max_length=100)
    institution = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    topics = tagulous.models.TagField(Topic, blank=True)

    def __str__(self):
        return self.title


class Certification(BaseStartDateEndDateModel):
    title = models.CharField(max_length=100)
    institution = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    topics = tagulous.models.TagField(Topic, blank=True)

    def __str__(self):
        return self.title


class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    github_url = models.URLField(null=True, blank=True)
    topics = tagulous.models.TagField(Topic, blank=True)

    def __str__(self):
        return self.title


def project_directory_path(instance, filename):
    project_name = slugify(instance.project.title)
    return os.path.join("projects", project_name, filename)


class Image(models.Model):
    project = models.ForeignKey(
        Project, related_name="project_images", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to=project_directory_path)

    def __str__(self):
        return f"Image for {self.project.title}"
