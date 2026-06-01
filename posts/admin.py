from django.contrib import admin
from posts.models import Post
from posts.models import Category

# Register your models here.

admin.site.register(Post)
admin.site.register(Category)
