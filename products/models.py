from django.db import models

class Brand(models.Model):
    name = models.CharField(max_length=100, verbose_name="Brand Name")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brands"

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Category Name")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Product Name")
    subtitle = models.CharField(max_length=255, blank=True, null=True, verbose_name="Subtitle")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")
    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        related_name='products',
        null=True,
        blank=True,
        verbose_name="Brand"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        null=True,
        blank=True,
        verbose_name="Category"
    )
    image = models.ImageField(upload_to='products/', null=True, blank=True, verbose_name="Product Image")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"