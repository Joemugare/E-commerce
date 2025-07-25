from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='products/', null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.name

class Price(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_price_id = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.product.name} - KSH {self.price}"

class MpesaPayment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    phone_number = models.CharField(max_length=15)
    transaction_id = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, default='Pending')
    checkout_request_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"M-Pesa Payment for {self.product.name} - {self.status}"

class StripePayment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_session_id = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Stripe Payment for {self.product.name} - {self.status}"
