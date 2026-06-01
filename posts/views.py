from django.shortcuts import render
from django.http.response import HttpResponse
from django.shortcuts import render
from posts.models import Post
from posts.models import Category
# Create your views here.


def hello_world(request):

    return HttpResponse("<h1>Hello world!</h1>")



def about(request):

    return render(request, "about.html")

def me(request):

    return HttpResponse("<h1>IT'S TEST!</h1>")

def post(request):
    post = Post.objects.all()

    text = ""
    for post in posts:
        text += f"<h1>{post.title}</h1> <br> {post.content}<br>"

    return HttpResponse(text)

def activate_categories_views(request):
    categories = Category.objects.filter(is_active=True)
    return render(request, "categories.html", {"categories": categories})