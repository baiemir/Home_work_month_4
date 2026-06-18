"""
URL configuration for blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from atexit import register

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from posts.views import about, home, me, get_detail, get_posts, activate_categories_views, category_detail, create_post, create_category, edit_post, my_post, delete_post
from users.views import register_user, login_user, logout_user
urlpatterns = [
    path('admin/', admin.site.urls),
    path("", home, name="home"),
    path("about/", about, name="about"),
    path("test/", me, name="test"),
    path("posts/", get_posts, name="posts"),
    path("categories/", activate_categories_views, name="categories"),
    path("post/<int:pk>/detail/", get_detail, name="post_detail"),
    path("post/<int:pk>/list/", get_posts, name="post_list"),
    path("category/<int:pk>/detail/", category_detail, name="category_detail"),
    path("post/create/", create_post, name="create_post"),
    path("category/create/", create_category, name="create_category"),
    path("users/register/", register_user, name="register"),
    path("users/login/", login_user, name="login"),
    path("users/logout/", logout_user, name="logout"),
    path("post/<int:pk>/edit/", edit_post, name="edit_post"),
    path("posts/my_post/", my_post, name="my_post"),
    path("post/<int:pk>/delete/", delete_post, name="delete_post")

]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)