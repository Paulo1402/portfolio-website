import io

from PIL.Image import Image
from PIL.ImageFile import ImageFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import ImageOps


def resize_and_pad_image(
    image: ImageFile, target_width=1100, target_height=800
) -> Image:
    target = (target_width, target_height)

    img = ImageOps.contain(image, target)  # Resize while keeping aspect ratio
    padded_img = ImageOps.pad(
        img,
        target,
    )

    return padded_img


def convert_image_to_inmemoryfile(
    image: ImageFile | Image, name: str, image_format: str
) -> InMemoryUploadedFile:
    output = io.BytesIO()

    image.save(output, format=image_format)
    output.seek(0)

    return InMemoryUploadedFile(
        output,
        "ImageField",
        name,
        f"image/{image_format}",
        output.getbuffer().nbytes,
        None,
    )
