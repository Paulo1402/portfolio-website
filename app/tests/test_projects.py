import tempfile
from datetime import date
from pathlib import Path

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from app.models import Project, ProjectImage


def create_project(title, start_date, **kwargs):
    defaults = {
        "description": f"{title} description",
        "start_date": start_date,
    }
    defaults.update(kwargs)

    return Project.objects.create(title=title, **defaults)


class ProjectsViewTests(TestCase):
    def setUp(self):
        self.media_dir = tempfile.TemporaryDirectory()
        self.override_media = override_settings(MEDIA_ROOT=Path(self.media_dir.name))
        self.override_media.enable()

    def tearDown(self):
        self.override_media.disable()
        self.media_dir.cleanup()

    def test_projects_page_renders_without_projects(self):
        response = self.client.get(reverse("projects"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Projects")

    def test_projects_are_ordered_by_newest_start_date(self):
        create_project("Older project", date(2023, 1, 1))
        create_project("Newer project", date(2024, 1, 1))

        response = self.client.get(reverse("projects"))

        self.assertContains(
            response,
            "Newer project",
            html=False,
        )
        self.assertLess(
            response.content.index(b"Newer project"),
            response.content.index(b"Older project"),
        )

    def test_projects_page_renders_six_projects_on_first_page(self):
        for index in range(7):
            create_project(f"Project {index}", date(2024, 1, index + 1))

        response = self.client.get(reverse("projects"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Project 6")
        self.assertContains(response, "Project 1")
        self.assertNotContains(response, "Project 0")

    def test_projects_page_renders_remaining_projects_on_second_page(self):
        for index in range(7):
            create_project(f"Project {index}", date(2024, 1, index + 1))

        response = self.client.get(reverse("projects"), {"page": "2"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Project 0")
        self.assertNotContains(response, "Project 6")

    def test_projects_page_uses_first_page_for_invalid_page_number(self):
        for index in range(7):
            create_project(f"Project {index}", date(2024, 1, index + 1))

        response = self.client.get(reverse("projects"), {"page": "invalid"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Project 6")
        self.assertNotContains(response, "Project 0")

    def test_projects_page_uses_last_page_for_out_of_range_page_number(self):
        for index in range(7):
            create_project(f"Project {index}", date(2024, 1, index + 1))

        response = self.client.get(reverse("projects"), {"page": "999"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Project 0")
        self.assertNotContains(response, "Project 6")

    def test_projects_page_renders_project_images_and_topics(self):
        project = create_project("Project with media", date(2024, 1, 1))
        project.topics = ["django", "postgres"]
        project.save()
        ProjectImage.objects.create(
            project=project,
            image=SimpleUploadedFile(
                "preview.png",
                b"image content",
                content_type="image/png",
            ),
        )

        response = self.client.get(reverse("projects"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "preview.png")
        self.assertContains(response, "django")
        self.assertContains(response, "postgres")
