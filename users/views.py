from django.shortcuts import render, redirect
from django.http.request import HttpRequest
from django.contrib.auth.models import User
from users.form import UserForm, LoginForm, forms
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
import uuid
from django.views.generic.edit import FormView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
# Create your views here.


class RegisterUserView(FormView):
    template_name = "users/register.html"
    form_class = UserForm
    success_url = "/"  # Куда перенаправить при успешной регистрации

    # Этот метод вызывается, если форма успешно прошла валидацию (is_valid)
    def form_valid(self, form):
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]
        
        try:
            # Создаем пользователя (в качестве username используем email, как в вашем коде)
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password
            )
            # Автоматически логиним пользователя после регистрации
            login(self.request, user)
            
            # Возвращаем стандартный редирект на success_url
            return super().form_valid(form)
            
        except IntegrityError:
            # Если такой email/username уже есть в базе
            form.add_error("email", "Пользователь с таким email уже существует")
            return self.form_invalid(form)

# def register_user(request):
#     form = UserForm()

#     if request.method == "POST":
#         form = UserForm(request.POST)
#         try:
#             if form.is_valid():
#                 email = form.cleaned_data["email"]
#                 password = form.cleaned_data["password"]
#                 user.username = uuid.uuid4()
#                 user = User.objects.create_user(
#                     username=email,
#                     email=email,
#                     password=password
#                 )

#                 login(request, user)
#                 return redirect("/")
#         except IntegrityError:
#             form.add_error("email", "Пользователь с таким email уже существует")
#     return render(request, "users/register.html", {"form": form})



class UserLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True  # ЗАМЕНЯЕТ ТВОЮ ПРОВЕРКУ: если вошел, кидает на главную
    
    # Переопределяем контекст, чтобы кастомизировать ошибку под ваш дизайн
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Если в форме есть ошибки (например, неверный пароль)
        if self.request.method == 'POST' and context['form'].errors:
            context['error'] = 'Неверный email или пароль'
            context['email'] = self.request.POST.get('username')  # Сохраняем введенный email
        return context
# def login_user(request: HttpRequest):
#     # Если пользователь уже авторизован, сразу кидаем на главную
#     if request.user.is_authenticated:
#         return redirect('/')

#     if request.method == "POST":
#         # Если вы используете кастомную форму, например LoginForm(request.POST)
#         # Получаем данные напрямую из POST запроса для надежности, раз мы входим по email
#         email = request.POST.get('email')
#         password = request.POST.get('password')

#         # ВАЖНО: Так как при регистрации мы записали email в поле username,
#         # здесь мы тоже ищем пользователя по полю username, передавая туда email!
#         user = authenticate(request, username=email, password=password)

#         if user is not None:
#             login(request, user)
#             return redirect('/')  # Успешный вход — переходим на главную
#         else:
#             # Если authenticate вернул None (пароль не подошел или пользователя нет)
#             context = {
#                 'error': 'Неверный email или пароль',
#                 'email': email # Чтобы email не стирался при перезагрузке
#             }
#             return render(request, 'users/login.html', context)

#     return render(request, 'users/login.html')


class UserLogoutView(LogoutView):
    # Куда перенаправить пользователя после выхода (вместо redirect('/'))
    next_page = reverse_lazy('home')  # или просто '/'
# def logout_user(request: HttpRequest):
#     # 1. Стираем пользователя из текущего запроса
#     auth_logout(request)
    
#     # 2. Принудительно очищаем и сбрасываем сессию в браузере
#     request.session.flush() 
    
#     # 3. Перенаправляем
#     return redirect('/')

