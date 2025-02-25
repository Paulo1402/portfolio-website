from django.db import models


class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    technologies = models.ManyToManyField("Technology")

    def __str__(self):
        return self.title


class Image(models.Model):
    project = models.ForeignKey(
        Project, related_name="images", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="img/")

    def __str__(self):
        return f"Image for {self.project.title}"


class Technology(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
