from django.db import models


# Create your models here.

class Tags(models.Model):
    name = models.CharField()

class Category(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.title

class Post(models.Model):
    title = models.CharField()
    content = models.TextField()
    rate = models.IntegerField()
    user = models.CharField(max_length=255, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField(Tags, null=True, blank=True)

    def __str__(self) -> str:
        name = self.category.name if self.category else "-"
        return f"{self.title} -- ({name})"

class Meta:
    verbose_name = "Post"
    verbose_name_plural = "Posts"


class Meta:
    verbose_name = "Category"
    verbose_name_plural = "Categories"





