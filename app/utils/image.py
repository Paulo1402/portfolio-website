import io

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models.fields.files import ImageFieldFile
from PIL import ImageOps
from PIL.Image import Image


def resize_and_pad_image(image: Image, target_width=1100, target_height=800) -> Image:
    target = (target_width, target_height)

    img = ImageOps.contain(image, target)  # Resize while keeping aspect ratio
    padded_img = ImageOps.pad(
        img,
        target,
    )

    return padded_img


def convert_image_to_inmemoryfile(
    image: Image, name: str, image_format: str
) -> InMemoryUploadedFile:
    output = io.BytesIO()
    pillow_format = get_pillow_image_format(image_format)
    content_type = get_image_content_type(image_format)

    image.save(output, format=pillow_format)
    output.seek(0)

    return InMemoryUploadedFile(
        output,
        "ImageField",
        name,
        content_type,
        output.getbuffer().nbytes,
        None,
    )


def get_image_content_type(image_format: str) -> str:
    normalized_format = get_pillow_image_format(image_format).lower()

    return f"image/{normalized_format}"


def get_pillow_image_format(image_format: str) -> str:
    normalized_format = image_format.upper()

    if normalized_format == "JPG":
        return "JPEG"

    return normalized_format


def get_max_image_dimensions(
    images: list[Image | ImageFieldFile],
) -> tuple[int, int]:
    if not images:
        raise ValueError("At least one image is required to get maximum dimensions.")

    width = 0
    height = 0

    for image in images:
        width = max(width, image.width)
        height = max(height, image.height)

    return width, height
