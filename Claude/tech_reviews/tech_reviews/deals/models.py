# deals/models.py
from django.db import models

class Deal(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='deals/', blank=True, null=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    deal_price = models.DecimalField(max_digits=10, decimal_places=2)
    link = models.URLField(max_length=500, blank=True, help_text="Enter the affiliate link (e.g., Amazon Associates URL with tracking ID).")
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.title

    def get_affiliate_link(self):
        affiliate_id = 'your_affiliate_id'  # Replace with your actual affiliate ID
        if self.link and 'amazon.com' in self.link and 'tag=' not in self.link:
            return f"{self.link}?tag={affiliate_id}"
        return self.link or '#'