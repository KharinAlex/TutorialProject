from django.views.generic.edit import FormView, UpdateView, DeleteView
from django.views.generic.base import View, TemplateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import UserModel
from .forms import ProfileForm


class RegisterFormView(FormView):
    form_class = UserCreationForm

    success_url = "/auth/login/"

    # Шаблон, который будет использоваться при отображении представления.
    template_name = "SignIn/registration.html"

    def form_valid(self, form):
        # Создаём пользователя, если данные в форму были введены корректно.
        form.save()

        # Вызываем метод базового класса
        return super(RegisterFormView, self).form_valid(form)


class LoginFormView(FormView):
    form_class = AuthenticationForm

    # Аналогично регистрации, только используем шаблон аутентификации.
    template_name = "SignIn/login.html"

    # В случае успеха перенаправим на главную.
    success_url = "/"

    def form_valid(self, form):
        # Получаем объект пользователя на основе введённых в форму данных.
        self.user = form.get_user()

        # Выполняем аутентификацию пользователя.
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)

        # После чего, перенаправляем пользователя на главную страницу.
        return HttpResponseRedirect("/")


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'SignIn/profile.html'

    def get_context_data(self, **kwargs):
        userModel = get_object_or_404(UserModel, user_id=self.request.user)
        context = super().get_context_data(**kwargs)
        context['user'] = userModel
        return context


class UserEdit(LoginRequiredMixin, UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email')
    template_name = "SignIn/edit_profile.html"

    def get_success_url(self):
        return reverse('Profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        form.save()
        return super(UserEdit, self).form_valid(form)


class ProfileEdit(LoginRequiredMixin, UpdateView):
    form_class = ProfileForm
    model = UserModel
    template_name = "SignIn/edit_profile.html"

    def get_success_url(self):
        return reverse('Profile')

    def get_object(self, queryset=None):
        return UserModel.objects.get(user_id=self.request.user)

    def form_valid(self, form):
        form.save()
        return super(ProfileEdit, self).form_valid(form)


class ProfileDelete(LoginRequiredMixin, DeleteView):
    model = User
    template_name = "SignIn/confirm_delete.html"
    success_url = '/'

    def get_object(self, queryset=None):
        return self.request.user

