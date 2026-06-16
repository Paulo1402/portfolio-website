import io
import logging
from dataclasses import dataclass
from urllib.parse import urlparse

import requests
from django.conf import settings
from PIL import Image, UnidentifiedImageError

from app.models import Project
from app.utils.image import (
    convert_image_to_inmemoryfile,
    get_max_image_dimensions,
    resize_and_pad_image,
)

logger = logging.getLogger(__name__)

GITHUB_API_BASE_URL = "https://api.github.com/repos"
GITHUB_REQUEST_TIMEOUT = 10
SUPPORTED_IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg")


class GitHubImportError(Exception):
    pass


class InvalidGitHubUrlError(GitHubImportError):
    pass


@dataclass(frozen=True)
class GitHubProjectImage:
    image: Image.Image
    name: str


@dataclass(frozen=True)
class GitHubImportResult:
    topics_count: int
    images_count: int


def parse_github_repository_url(github_url: str | None) -> str:
    return GitHubProjectImporter.parse_repository_url(github_url)


def import_project_from_github(project: Project) -> GitHubImportResult:
    return GitHubProjectImporter(project).import_project()


class GitHubProjectImporter:
    def __init__(self, project: Project):
        self.project = project

    def import_project(self) -> GitHubImportResult:
        repository = self.parse_repository_url(self.project.github_url)
        topics = self._fetch_repository_topics(repository)
        self.project.topics = self._merge_topics(topics)

        images = self._fetch_project_images(repository)
        self._save_project_images(images)

        self.project.save()

        return GitHubImportResult(topics_count=len(topics), images_count=len(images))

    @staticmethod
    def parse_repository_url(github_url: str | None) -> str:
        if not github_url:
            raise InvalidGitHubUrlError("Project does not have a GitHub URL.")

        parsed_url = urlparse(github_url.strip())
        hostname = parsed_url.hostname or ""
        path_parts = [part for part in parsed_url.path.split("/") if part]

        if hostname.lower() != "github.com" or len(path_parts) < 2:
            raise InvalidGitHubUrlError("Project GitHub URL must point to a repository.")

        owner, repo = path_parts[:2]
        repo = repo.removesuffix(".git")

        if not owner or not repo:
            raise InvalidGitHubUrlError("Project GitHub URL must point to a repository.")

        return f"{owner}/{repo}"

    def _fetch_repository_topics(self, repository: str) -> list[str]:
        response = self._github_get(f"{GITHUB_API_BASE_URL}/{repository}")

        try:
            response.raise_for_status()
            response_json = response.json()
        except requests.RequestException as error:
            raise GitHubImportError("Failed to fetch GitHub repository data.") from error
        except ValueError as error:
            raise GitHubImportError("GitHub repository response is invalid.") from error

        if not isinstance(response_json, dict):
            raise GitHubImportError("GitHub repository response is invalid.")

        topics = response_json.get("topics")

        if topics is None:
            return []

        if not isinstance(topics, list):
            raise GitHubImportError("GitHub repository topics response is invalid.")

        return [str(topic) for topic in topics]

    def _merge_topics(self, topics: list[str]) -> list[str]:
        merged_topics = []

        for topic in [*self.project.topics.all(), *topics]:
            topic_name = str(topic)

            if topic_name not in merged_topics:
                merged_topics.append(topic_name)

        return merged_topics

    def _fetch_project_images(self, repository: str) -> list[GitHubProjectImage]:
        response = self._github_get(f"{GITHUB_API_BASE_URL}/{repository}/contents/.github")

        if response.status_code == 404:
            return []

        try:
            response.raise_for_status()
            response_json = response.json()
        except requests.RequestException as error:
            raise GitHubImportError("Failed to fetch GitHub project images.") from error
        except ValueError as error:
            raise GitHubImportError("GitHub project images response is invalid.") from error

        if not isinstance(response_json, list):
            raise GitHubImportError("GitHub project images response is invalid.")

        project_images = []

        for content in response_json:
            if not isinstance(content, dict):
                continue

            content_name = content.get("name", "")

            if not self._is_supported_image(content_name):
                continue

            image = self._fetch_image(content.get("download_url"), content_name)

            if image:
                project_images.append(image)

        return project_images

    def _fetch_image(
        self, download_url: str | None, content_name: str
    ) -> GitHubProjectImage | None:
        if not download_url:
            return None

        try:
            response = self._github_get(download_url)
            response.raise_for_status()
            image = Image.open(io.BytesIO(response.content))
        except (requests.RequestException, UnidentifiedImageError, OSError):
            logger.warning("Failed to fetch GitHub project image: %s", content_name)
            return None

        return GitHubProjectImage(image=image, name=content_name)

    def _save_project_images(self, images: list[GitHubProjectImage]) -> None:
        if not images:
            return

        width, height = get_max_image_dimensions([image.image for image in images])

        for image in images:
            resized_image = resize_and_pad_image(image.image, width, height)
            inmemory_image = convert_image_to_inmemoryfile(
                resized_image,
                image.name,
                image_format=image.image.format,
            )
            project_image = self.project.project_images.filter(
                image__endswith=image.name
            ).first()

            if project_image:
                project_image.image = inmemory_image
                project_image.save()
            else:
                self.project.project_images.create(image=inmemory_image)

    @staticmethod
    def _is_supported_image(filename: str) -> bool:
        return filename.lower().endswith(SUPPORTED_IMAGE_EXTENSIONS)

    def _github_get(self, url: str) -> requests.Response:
        return requests.get(
            url,
            headers=self._github_headers(),
            timeout=GITHUB_REQUEST_TIMEOUT,
        )

    @staticmethod
    def _github_headers() -> dict[str, str]:
        if not settings.GITHUB_TOKEN:
            return {}

        return {"Authorization": f"Bearer {settings.GITHUB_TOKEN}"}
