# reviews/models.py
from django.db import models
from django.contrib.auth.models import User
from products.models import Product

class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_user_reviews')
    title = models.CharField(max_length=200)
    comment = models.TextField()
    rating = models.IntegerField()
    video_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title