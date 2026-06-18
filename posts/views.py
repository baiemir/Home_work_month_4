from django.shortcuts import render
from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from posts.models import Post, Category
from django.http import HttpRequest
from posts.form import PostForm, CategoryModelForm, PostEditForm
from django.contrib.auth.decorators import login_required
# Create your views here.


def home(request):
    all_posts = Post.objects.all().order_by("-create_at")
    return render(request, "base.html", context={"posts": all_posts})
    


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

def create_post(request):
    categoies = Category.objects.all()
    category_form = CategoryModelForm()
    if request.method == "POST":
         # логика создания поста
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            post = Post(
                title=cleaned_data.get('title'), 
                content=cleaned_data.get('content'), 
                image=cleaned_data.get('image'), 
                category=cleaned_data.get('category'), 
                rate=5
                )
            if request.user.is_authenticated:
                post.user = request.user

            post.save()
            return redirect('posts') # перенаправляем на страницу со списком постов после создания
        context = {
                "categories": categoies,
                "category_form": category_form,
            }
        return render(request, "posts/create_post.html", context={"errors": form.errors}) # если форма не валидна, возвращаем её с ошибками
    form = PostForm()
    context = {
        "form": form,
        "categories": categoies,
        "category_form": category_form,
    }
    return render(request, "posts/create_post.html", context=context)

def create_category(request):
    if request.method == "POST":
        form = CategoryModelForm(request.POST, request.FILES)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            category =Category(
                title = cleaned_data.get('title'),
                description = cleaned_data.get('description'),
                is_active = cleaned_data.get('is_active'),
            )
            category.save()
            return redirect('create_post') # перенаправляем на страницу со списком категорий после создания
        return render(request, "posts/create_post.html", context={"errors": form.errors}) # если форма не валидна, возвращаем её с ошибками
    return render(request, "posts/create_post.html")

def edit_post(request: HttpRequest, pk):
    post = get_object_or_404(Post, pk=pk)

    
    if request.method == "POST":
        #form = PostEditForm(request.POST, request.FILES)
        # Тут твоя логика сохранения измененного поста...
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        # ... и так далее ...
        post.save()
        return redirect('/')
        #if form.is_valid():
            #cleaned_data = form.cleaned_data
            #post.title = cleaned_data["title"]
            #post.content = cleaned_data["content"]
            #post.image = cleaned_data["image"]
            #post.rate = cleaned_data["image"]
            #return redirect("/")
    #form = PostEditForm(post)
    return render(request, "posts/edit.html", {"post": post})

@login_required(login_url='login')
def my_post(request: HttpRequest):
    user_posts = Post.objects.filter(user=request.user).order_by("-create_at")
    return render(request, "posts/my_post.html", context={"posts": user_posts})

@login_required(login_url='login')
def delete_post(request: HttpRequest, pk):
    # 1. Ищем пост в базе данных по его id (pk)
    post = get_object_or_404(Post, pk=pk)
    
    # 2. ПРОВЕРКА USER'А (Самое важное из твоего ДЗ!)
    if post.user == request.user:
        post.delete()  # Удаляем пост из базы данных
    
    # 3. Перенаправление
    # Здесь можно вернуть пользователя обратно на страницу его постов
        return redirect('my_post')
    # Если чужой попытался удалить — просто проигнорировать или выдать ошибку
    else:
        return HttpResponse("ВЫ не можете удалить чужой пост!", status=403)




