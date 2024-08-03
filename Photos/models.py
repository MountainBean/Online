from django.db import models
from django.core.files.storage import default_storage
from django.db.models.fields.files import ImageFieldFile, FileField
from io import BytesIO
from os.path import basename
from PIL import Image


class Photographer(models.Model):
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self) -> str:
        return self.full_name()


class Photo(models.Model):
    title = models.CharField(max_length=256)
    location = models.CharField(max_length=80)
    image = models.ImageField(upload_to="images", null=True)
    image_small = models.ImageField(
        upload_to="images/small",
        null=True,
        editable=False)
    # image_thumbnail = models.CharField(max_length=256, null=True)
    photographer = models.ForeignKey(
        Photographer,
        on_delete=models.CASCADE,
        null=True,
        related_name="photos")
    date = models.DateField()
    slug = models.SlugField(default="", null=False)

    def __str__(self):
        return f"{self.title} - {self.photographer}, {self.date}"

    def save(self, *args, **kwargs):
        """
        Overwriting because we need to save a image_small and image_thumbnail.
        """
        image_object = getattr(self, "image")
        image_small = getattr(self, "image_small")
        if image_small.name is None:
            self.generate_small_image(image_object)

        super().save(*args, **kwargs)

    def generate_small_image(self, image_object: ImageFieldFile):
        """
        create a smaller copy of the image file and save it as the
        image_small for this model object

        Args:
            image_object (ImageFieldFile): The Image selected in the ImageFileField
        """

        rgb_image = Image.open(image_object.file.file)
        original_width, original_height = rgb_image.size

        if original_width < 720 or original_height < 720:
            # original image is already too small...
            smaller_image = image_object.file.file
        else:
            if original_width < original_height:
                new_width = 720
                new_height = int(original_height *
                                 (new_width / original_width))
            else:
                new_height = 720
                new_width = int(original_width *
                                (new_height / original_height))
            smaller_image = rgb_image.resize((new_width, new_height))

        smaller_image_file = BytesIO()
        smaller_image.save(smaller_image_file, "JPEG")

        # Save new "smaller" image in image/small directory
        base_name = basename(image_object.name)
        file_name = default_storage.save(
            "images/small/"+base_name, smaller_image_file)
        # Update image_small field with the new file location
        self.image_small.file = ImageFieldFile(
            instance=None, field=FileField(), name=file_name)
        self.image_small.name = file_name
