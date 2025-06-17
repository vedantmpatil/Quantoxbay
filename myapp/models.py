from django.db import models
from django.contrib.auth.models import User
from cloudinary_storage.storage import MediaCloudinaryStorage



class Product(models.Model):

    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=100)
    
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    file = models.FileField(upload_to='uploads/products/',storage=MediaCloudinaryStorage())
    file_size = models.CharField(max_length=20, blank=True)
    file_type = models.CharField(max_length=50, blank=True)
    
    thumbnail = models.ImageField(upload_to='uploads/thumbnails/',storage=MediaCloudinaryStorage(), null=True, blank=True)
    preview_url = models.URLField(blank=True)

    tags = models.CharField(max_length=200, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    total_sales_count = models.IntegerField(default=0)
    total_sales_amount = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.file:
            self.file_size = f"{round(self.file.size / 1024, 2)} KB"
            self.file_type = self.file.name.split('.')[-1].lower()
            # Save again with updated metadata
            super().save(update_fields=['file_size', 'file_type'])

            # Debug print
            print("📦 File storage backend:", self.file.storage)
            print("📦 File URL:", self.file.url)


    def __str__(self):
        return self.title


class OrderDetail(models.Model):
    customer_email = models.EmailField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField()
    stripe_payment_intent = models.CharField(max_length=255, null=True, blank=True)
    has_paid = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)