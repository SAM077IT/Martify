from django.db import models
import datetime


class BlogCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Blog Categories'


class Blog(models.Model):
    title = models.CharField(max_length=255)
    post_body = models.TextField(blank=True)
    author = models.CharField(max_length=200)
    image = models.ImageField(
        upload_to='uploads/blog/', blank=True, default="uploads/product/no-image.jpg")
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(
        BlogCategory, on_delete=models.CASCADE, default='Universal')

    # def __str__(self):
    #     return self.title
