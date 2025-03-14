import os

import tagulous.models
from django.db import models
from django.utils.text import slugify

from app.models.base import BaseStartDateEndDateModel
from app.models.topic import Topic


class Project(BaseStartDateEndDateModel):
    title = models.CharField(max_length=100)
    company = models.CharField(max_length=100, default="Projeto Pessoal")
    description = models.TextField()
    github_url = models.URLField(null=True, blank=True)
    topics = tagulous.models.TagField(Topic, blank=True)

    def __str__(self):
        return self.title


def project_directory_path(instance, filename):
    project_name = slugify(instance.project.title)
    return os.path.join("projects", project_name, filename)


class ProjectImage(models.Model):
    project = models.ForeignKey(
        Project, related_name="project_images", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to=project_directory_path)

    def __str__(self):
        return f"Image for {self.project.title}"
