from django.db import models
from categories.models import Category
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

class Product(models.Model):
    name = models.CharField(max_length=255)
    short_description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='products'
    )
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    image_small = models.ImageField(upload_to='products/small/', blank=True, null=True)
    in_stock = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.image and not self.image_small:
            try:
                # Open the uploaded image
                img = Image.open(self.image)
                max_size = (100, 100)  # Target size for small image
                img.thumbnail(max_size, Image.Resampling.LANCZOS)

                # Save the resized image to image_small
                output = BytesIO()
                img_format = img.format if img.format else 'JPEG'
                img.save(output, format=img_format, quality=85)
                output.seek(0)
                self.image_small = InMemoryUploadedFile(
                    output,
                    'ImageField',
                    f"small_{self.image.name.split('/')[-1]}",
                    f'image/{img_format.lower()}',
                    output.getbuffer().nbytes,
                    None
                )
            except Exception as e:
                print(f"Error resizing image for {self.name}: {e}")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name