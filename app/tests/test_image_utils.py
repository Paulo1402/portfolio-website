from datetime import date
from unittest.mock import patch

from django.test import TestCase
from PIL import Image

from app.admin.project import ProjectAdmin
from app.models import Project
from app.utils.image import convert_image_to_inmemoryfile, get_max_image_dimensions


def create_image(width, height, image_format="PNG"):
    image = Image.new("RGB", (width, height), color="red")
    image.format = image_format

    return image


class ImageUtilsTests(TestCase):
    def test_get_max_image_dimensions_tracks_width_and_height_independently(self):
        images = [
            create_image(100, 400),
            create_image(300, 200),
        ]

        self.assertEqual(get_max_image_dimensions(images), (300, 400))

    def test_get_max_image_dimensions_returns_single_image_dimensions(self):
        image = create_image(120, 80)

        self.assertEqual(get_max_image_dimensions([image]), (120, 80))

    def test_get_max_image_dimensions_requires_at_least_one_image(self):
        with self.assertRaisesRegex(ValueError, "At least one image is required"):
            get_max_image_dimensions([])

    def test_convert_image_to_inmemoryfile_uses_png_content_type(self):
        image_file = convert_image_to_inmemoryfile(
            create_image(10, 10, "PNG"),
            "preview.png",
            image_format="PNG",
        )

        self.assertEqual(image_file.content_type, "image/png")

    def test_convert_image_to_inmemoryfile_uses_jpeg_content_type(self):
        image_file = convert_image_to_inmemoryfile(
            create_image(10, 10, "JPEG"),
            "preview.jpeg",
            image_format="JPEG",
        )

        self.assertEqual(image_file.content_type, "image/jpeg")

    def test_convert_image_to_inmemoryfile_normalizes_jpg_content_type(self):
        image_file = convert_image_to_inmemoryfile(
            create_image(10, 10, "JPEG"),
            "preview.jpg",
            image_format="JPG",
        )

        self.assertEqual(image_file.content_type, "image/jpeg")


class ProjectAdminImageResizeTests(TestCase):
    @patch("app.admin.project.get_max_image_dimensions")
    def test_resize_and_pad_images_returns_early_without_images(self, mock_get_dimensions):
        ProjectAdmin.resize_and_pad_images([])

        mock_get_dimensions.assert_not_called()

    def test_resize_and_pad_images_accepts_project_without_images(self):
        project = Project.objects.create(
            title="Portfolio",
            description="Personal portfolio.",
            start_date=date(2024, 1, 1),
        )

        ProjectAdmin.resize_and_pad_images(list(project.project_images.all()))
