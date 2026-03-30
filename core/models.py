from django.db import models
import datetime
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(
        upload_to='uploads/category/', default="uploads/product/no-image.jpg")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    off_percent = models.IntegerField(default=0, blank=True)
    image = models.ImageField(upload_to='uploads/product/')
    image_secondry = models.ImageField(
        upload_to='uploads/product/', blank=True, default="uploads/product/no-image.jpg")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, default='Universal')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, default='Martify', )
    sku = models.CharField(max_length=255)
    created_at = models.DateField(default=datetime.date.today)
    description = models.TextField(blank=True, null=True)

    # def __str__(self):
    #     return self.name

    @property
    def sale_price(self):
        """Calculate the sale price if off_percent is set."""
        if self.off_percent and self.off_percent > 0:
            return round(self.price * (1 - self.off_percent / 100), 2)
        return None
