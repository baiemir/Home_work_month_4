from django.db import models


# Create your models here.

class Post(models.Model):
    title = models.CharField()
    content = models.TextField()
    rate = models.IntegerField()
    user = models.CharField(max_length=255, null=True, blank=True)

class Meta:
    verbose_name = "Post"
    verbose_name_plural = "Posts"

class Category(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    is_active = models.BooleanField(default=True)

class Meta:
    verbose_name = "Category"
    verbose_name_plural = "Categories"





