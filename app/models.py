from django.db import models


class About(models.Model):
    description = models.TextField()
    technologies = models.ManyToManyField("Technology")

    def __str__(self):
        return "About"


class Experience(models.Model):
    title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()
    technologies = models.ManyToManyField("Technology")

    def __str__(self):
        return self.title


class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    technologies = models.ManyToManyField("Technology")
    topics = models.ManyToManyField("Topic")
    github_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.title


class Image(models.Model):
    project = models.ForeignKey(
        Project, related_name="project_images", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="project/")

    def __str__(self):
        return f"Image for {self.project.title}"


class Formation(models.Model):
    title = models.CharField(max_length=100)
    institution = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()

    def __str__(self):
        return self.title


class Certification(models.Model):
    title = models.CharField(max_length=100)
    institution = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class Technology(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Topic(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
