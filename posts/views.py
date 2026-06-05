from django.shortcuts import render
from django.http.response import HttpResponse
from django.shortcuts import render
from posts.models import Post, Category
# Create your views here.


def home(request):

    return render(request, "base.html")


def about(request):

    return render(request, "about.html")

def me(request):

    return HttpResponse("<h1>IT'S TEST!</h1>")

def post(request):
    posts = Post.objects.all()

    text = ""
    for post in posts:
        text += f"<h1>{post.title}</h1> <br> {post.content}<br>"

    return HttpResponse(text)

def activate_categories_views(request):
    categories = Category.objects.filter(is_active=True)
    return render(request, "categories.html", {"categories": categories})

def get_posts(request, pk=None):
    if pk is not None:
        posts = Post.objects.filter(id=pk)
    else:
        posts = Post.objects.all()
    return render(request, "posts/post_list.html", context={"posts": posts, "categories": Category.objects.filter(is_active=True)})


def get_detail(request, pk):
    post = Post.objects.get(id=pk)
    return render(request, "posts/post_detail.html", context={"post": post})

def category_detail(request, pk):
    category = Category.objects.get(id=pk)
    category_posts = category.post_set.all()
    context = {
        "categories": Category.objects.filter(is_active=True),
        "category": category,
        "category_posts": category_posts
    }
    return render(request, "categories/category_detail.html", context=context)