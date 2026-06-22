from django.shortcuts import render
from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from posts.models import Post, Category
from django.http import HttpRequest
from posts.form import PostForm, CategoryModelForm, PostEditForm, PostModelForm
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.forms.models import BaseModelForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
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

# def get_posts(request, pk=None):
#     if pk is not None:
#         posts = Post.objects.filter(id=pk)
#     else:
#         posts = Post.objects.all()
#     return render(request, "posts/post_list.html", context={"posts": posts, "categories": Category.objects.filter(is_active=True)})

# Создаем класс-представление (Class Based View)
# Он заменяет обычную функцию вида:
#
# def post_list(request):
#     posts = Post.objects.all()
#     return render(request, "posts/post_list.html", {"posts": posts})
#
class PostListView(ListView):

    # Указываем модель, с которой будет работать представление.
    # Django автоматически выполнит запрос:
    # Post.objects.all()
    model = Post

    # Можно явно указать запрос.
    # Если написать queryset, то будет использоваться он,
    # а не автоматически созданный запрос из model.
    #
    # queryset = Post.objects.all()
    #
    # Например:
    # queryset = Post.objects.filter(is_active=True)

    # Шаблон, который будет отображаться пользователю.
    # Django возьмет данные из модели и передаст их в этот HTML-файл.
    template_name = "posts/post_list.html"

    # Имя переменной, которая попадет в шаблон.
    #
    # По умолчанию Django создает object_list.
    #
    # Тогда в шаблоне пришлось бы писать:
    # {% for post in object_list %}
    #
    # Но мы задаем более понятное имя:
    context_object_name = "posts"

    # Теперь в шаблоне можно писать:
    #
    # {% for post in posts %}
    #     <h2>{{ post.title }}</h2>
    # {% endfor %}

    # Теперь в шаблоне можно писать:
    #
    # {% for post in posts %}
    #     <h2>{{ post.title }}</h2>
    # {% endfor %}
    def get_queryset(self):
        queryset = super().get_queryset().order_by('-id')
        search_query = self.request.GET.get('search', '')
        
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | 
                Q(content__icontains=search_query)
            )
        return queryset

# def get_detail(request, pk):
#     post = Post.objects.get(id=pk)
#     return render(request, "posts/post_detail.html", context={"post": post})

class PostDetailView(DetailView):
    model = Post
    template_name = "posts/post_detail.html"
    context_object_name = "post"



def category_detail(request, pk):
    category = Category.objects.get(id=pk)
    category_posts = category.post_set.all()
    context = {
        "categories": Category.objects.filter(is_active=True),
        "category": category,
        "category_posts": category_posts
    }
    return render(request, "categories/category_detail.html", context=context)

# def create_post(request):
#     categories = Category.objects.all()
#     category_form = CategoryModelForm()
#     if request.method == "POST":
#          # логика создания поста
#         form = PostForm(request.POST, request.FILES)
#         if form.is_valid():
#             cleaned_data = form.cleaned_data
#             post = Post(
#                 title=cleaned_data.get('title'), 
#                 content=cleaned_data.get('content'), 
#                 image=cleaned_data.get('image'), 
#                 category=cleaned_data.get('category'), 
#                 rate=5
#                 )
#             if request.user.is_authenticated:
#                 post.user = request.user

#             post.save()
#             return redirect('posts') # перенаправляем на страницу со списком постов после создания
#         context = {
#                 "categories": categories,
#                 "category_form": category_form,
#             }
#         return render(request, "posts/create_post.html", context={"errors": form.errors}) # если форма не валидна, возвращаем её с ошибками
#     form = PostForm()
#     context = {
#         "form": form,
#         "categories": categories,
#         "category_form": category_form,
#     }
#     return render(request, "posts/create_post.html", context=context)

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostModelForm  # Основная форма (для Поста)
    template_name = 'posts/create_post.html'  # Имя вашего HTML-файла
    success_url = reverse_lazy('home')  # Куда перенаправлять при успехе

    def get(self, request: HttpRequest, *args: str, **kwargs) -> HttpResponse:
        if self.request.user.is_anonymous:
            return redirect("login")
        return super().get(request, *args, **kwargs)

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.user = self.request.user
        return super().form_valid(form)

    # Шаг 1: Переопределяем метод получения контекста, 
    # чтобы передать форму категории и список категорий в шаблон
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Передаем список активных категорий для выпадающего списка
        context['categories'] = Category.objects.filter(is_active=True)
        # Передаем пустую форму категории под именем 'category_form' (как в HTML)
        context['create_post'] = CategoryModelForm()
        return context

    # Шаг 2: Переопределяем обработку POST-запросов, 
    # так как на этот класс будут приходить запросы от двух РАЗНЫХ форм
    def post(self, request, *args, **kwargs):
        
        # Проверяем, пришел ли запрос от формы создания КАТЕГОРИИ.
        # В вашей HTML-форме категории отправляются поля 'title' и 'description'
        # Но мы можем отловить этот запрос по специфичному URL или по наличию полей.
        # Поскольку у вас в HTML action="{% url 'create_category' %}", 
        # этот метод сработает, если оба URL ведут на этот класс.
        
        # Если в запросе передано поле 'description', значит это форма категории
        if 'description' in request.POST:
            category_form = CategoryModelForm(request.POST)
            if category_form.is_valid():
                category_form.save()
                # После успешного создания перенаправляем пользователя на эту же страницу,
                # чтобы выпадающий список обновился, и категория там появилась
                return redirect(request.path)
            else:
                # Если в форме категории были ошибки, перерисовываем страницу с ними
                self.object = None
                context = self.get_context_data()
                context['category_form'] = category_form
                return self.render_to_response(context)

        # Если это не категория, значит создается обычный ПОСТ.
        # Отдаем управление стандартному поведению Джанго (классу CreateView)
        return super().post(request, *args, **kwargs)

# def create_category(request):
#     if request.method == "POST":
#         form = CategoryModelForm(request.POST, request.FILES)
#         if form.is_valid():
#             cleaned_data = form.cleaned_data
#             category =Category(
#                 title = cleaned_data.get('title'),
#                 description = cleaned_data.get('description'),
#                 is_active = cleaned_data.get('is_active'),
#                 )
#             category.save()
#             return redirect('create_post') # перенаправляем на страницу со списком категорий после создания
#         return render(request, "posts/create_post.html", context={"errors": form.errors}) # если форма не валидна, возвращаем её с ошибками
#     return render(request, "posts/create_post.html")


class PostUpdateView(UpdateView):
    model = Post
    template_name = 'posts/edit.html'
    context_object_name = 'post'  # Передает объект в шаблон как {{ post }}
    success_url = reverse_lazy('home')  # Аналог вашего redirect('/')

    # ВАРИАНТ 1: Если у вас есть готовый класс формы (раскомментируйте строку ниже)
    # form_class = PostEditForm

    # ВАРИАНТ 2: Если формы нет, можно прямо тут указать нужные поля, и Django создаст форму сам:
    fields = ['title', 'content', 'image', 'rate']

# def edit_post(request: HttpRequest, pk):
#     post = get_object_or_404(Post, pk=pk)

        
#     if request.method == "POST":
#         #form = PostEditForm(request.POST, request.FILES)
#         # Тут твоя логика сохранения измененного поста...
#         post.title = request.POST.get('title')
#         post.content = request.POST.get('content')
#         # ... и так далее ...
#         post.save()
#         return redirect('/')
#         #if form.is_valid():
#             #cleaned_data = form.cleaned_data
#             #post.title = cleaned_data["title"]
#             #post.content = cleaned_data["content"]
#             #post.image = cleaned_data["image"]
#             #post.rate = cleaned_data["image"]
#             #return redirect("/")
#     #form = PostEditForm(post)
#     return render(request, "posts/edit.html", {"post": post})

@login_required(login_url='login')
def my_post(request: HttpRequest):
    user_posts = Post.objects.filter(user=request.user).order_by("-create_at")
    return render(request, "posts/my_post.html", context={"posts": user_posts})

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin, DeleteView):
    model = Post
    # Куда перенаправить пользователя после успешного удаления
    success_url = reverse_lazy('my_post') 
    
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    # 1. ПРОВЕРКА USER'А (Самое важное из твоего ДЗ!)
    def test_func(self):
        # Получаем сам объект поста, который пытаются удалить
        post = self.get_object()
        # Проверяем, совпадает ли автор поста с текущим пользователем
        return post.user == self.request.user

    # 2. Что делать, если проверка не пройдена (Вместо стандартного 403)
    def handle_no_permission(self):
        return HttpResponse("Вы не можете удалить чужой пост!", status=403)

# def delete_post(request: HttpRequest, pk):
#     # 1. Ищем пост в базе данных по его id (pk)
#     post = get_object_or_404(Post, pk=pk)
    
#     # 2. ПРОВЕРКА USER'А (Самое важное из твоего ДЗ!)
#     if post.user == request.user:
#         post.delete()  # Удаляем пост из базы данных
    
#     # 3. Перенаправление
#     # Здесь можно вернуть пользователя обратно на страницу его постов
#         return redirect('my_post')
#     # Если чужой попытался удалить — просто проигнорировать или выдать ошибку
#     else:
#         return HttpResponse("ВЫ не можете удалить чужой пост!", status=403)




