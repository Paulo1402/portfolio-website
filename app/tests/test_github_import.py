import io
import tempfile
from datetime import date
from pathlib import Path
from unittest.mock import patch

import requests
from django.test import TestCase, override_settings
from PIL import Image

from app.models import Project
from app.utils.github import (
    GITHUB_REQUEST_TIMEOUT,
    GitHubImportError,
    InvalidGitHubUrlError,
    import_project_from_github,
    parse_github_repository_url,
)


class FakeGitHubResponse:
    def __init__(self, status_code=200, json_data=None, content=b""):
        self.status_code = status_code
        self.json_data = json_data
        self.content = content

    def json(self):
        return self.json_data

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"{self.status_code} error")


def create_project(**kwargs):
    defaults = {
        "title": "Portfolio Website",
        "description": "Personal portfolio.",
        "start_date": date(2024, 1, 1),
    }
    defaults.update(kwargs)

    return Project.objects.create(**defaults)


def png_bytes():
    output = io.BytesIO()
    Image.new("RGB", (20, 10), color="red").save(output, format="PNG")
    return output.getvalue()


class GitHubRepositoryUrlParserTests(TestCase):
    def test_parses_valid_github_repository_url(self):
        repository = parse_github_repository_url("https://github.com/paulo/site")

        self.assertEqual(repository, "paulo/site")

    def test_parses_url_with_trailing_slash(self):
        repository = parse_github_repository_url("https://github.com/paulo/site/")

        self.assertEqual(repository, "paulo/site")

    def test_parses_url_with_query_string_and_fragment(self):
        repository = parse_github_repository_url(
            "https://github.com/paulo/site?tab=readme#install"
        )

        self.assertEqual(repository, "paulo/site")

    def test_rejects_missing_url(self):
        with self.assertRaises(InvalidGitHubUrlError):
            parse_github_repository_url("")

    def test_rejects_non_github_url(self):
        with self.assertRaises(InvalidGitHubUrlError):
            parse_github_repository_url("https://example.com/paulo/site")

    def test_rejects_github_url_without_repository(self):
        with self.assertRaises(InvalidGitHubUrlError):
            parse_github_repository_url("https://github.com/paulo")


class GitHubProjectImportTests(TestCase):
    def setUp(self):
        self.media_dir = tempfile.TemporaryDirectory()
        self.override_media = override_settings(MEDIA_ROOT=Path(self.media_dir.name))
        self.override_media.enable()

    def tearDown(self):
        self.override_media.disable()
        self.media_dir.cleanup()

    @patch("app.utils.github.requests.get")
    def test_missing_github_url_makes_no_request(self, mock_get):
        project = create_project(github_url="")

        with self.assertRaises(InvalidGitHubUrlError):
            import_project_from_github(project)

        mock_get.assert_not_called()

    @patch("app.utils.github.requests.get")
    def test_repository_api_failure_is_handled(self, mock_get):
        project = create_project(github_url="https://github.com/paulo/site")
        mock_get.return_value = FakeGitHubResponse(status_code=500)

        with self.assertRaisesRegex(
            GitHubImportError, "Failed to fetch GitHub repository data."
        ):
            import_project_from_github(project)

    @patch("app.utils.github.requests.get")
    def test_valid_repository_without_images_updates_topics(self, mock_get):
        project = create_project(github_url="https://github.com/paulo/site")
        project.topics = ["django"]
        project.save()
        mock_get.side_effect = [
            FakeGitHubResponse(json_data={"topics": ["django", "python"]}),
            FakeGitHubResponse(status_code=404),
        ]

        result = import_project_from_github(project)

        project.refresh_from_db()
        self.assertEqual(result.topics_count, 2)
        self.assertEqual(result.images_count, 0)
        self.assertEqual([str(topic) for topic in project.topics.all()], ["django", "python"])
        self.assertEqual(project.project_images.count(), 0)

    @patch("app.utils.github.requests.get")
    def test_invalid_project_image_is_skipped(self, mock_get):
        project = create_project(github_url="https://github.com/paulo/site")
        mock_get.side_effect = [
            FakeGitHubResponse(json_data={"topics": []}),
            FakeGitHubResponse(
                json_data=[
                    {
                        "name": "preview.png",
                        "download_url": "https://raw.example/preview.png",
                    }
                ]
            ),
            FakeGitHubResponse(content=b"not an image"),
        ]

        result = import_project_from_github(project)

        self.assertEqual(result.images_count, 0)
        self.assertEqual(project.project_images.count(), 0)

    @patch("app.utils.github.requests.get")
    def test_image_download_failure_is_skipped(self, mock_get):
        project = create_project(github_url="https://github.com/paulo/site")
        mock_get.side_effect = [
            FakeGitHubResponse(json_data={"topics": []}),
            FakeGitHubResponse(
                json_data=[
                    {
                        "name": "preview.png",
                        "download_url": "https://raw.example/preview.png",
                    }
                ]
            ),
            FakeGitHubResponse(status_code=503),
        ]

        result = import_project_from_github(project)

        self.assertEqual(result.images_count, 0)
        self.assertEqual(project.project_images.count(), 0)

    @patch("app.utils.github.requests.get")
    def test_valid_project_image_is_imported(self, mock_get):
        project = create_project(github_url="https://github.com/paulo/site")
        mock_get.side_effect = [
            FakeGitHubResponse(json_data={"topics": []}),
            FakeGitHubResponse(
                json_data=[
                    {
                        "name": "preview.png",
                        "download_url": "https://raw.example/preview.png",
                    }
                ]
            ),
            FakeGitHubResponse(content=png_bytes()),
        ]

        result = import_project_from_github(project)

        self.assertEqual(result.images_count, 1)
        self.assertEqual(project.project_images.count(), 1)
        self.assertTrue(project.project_images.first().image.name.endswith("preview.png"))

    @patch("app.utils.github.requests.get")
    def test_requests_use_timeout(self, mock_get):
        project = create_project(github_url="https://github.com/paulo/site")
        mock_get.side_effect = [
            FakeGitHubResponse(json_data={"topics": []}),
            FakeGitHubResponse(status_code=404),
        ]

        import_project_from_github(project)

        self.assertEqual(mock_get.call_count, 2)

        for call in mock_get.call_args_list:
            self.assertEqual(call.kwargs["timeout"], GITHUB_REQUEST_TIMEOUT)
