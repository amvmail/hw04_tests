#  yatube/users/views.py
# Импортируем CreateView, чтобы создать ему наследника
# Функция reverse_lazy позволяет получить URL по параметрам функции path()
# Берём, тоже пригодится
# Импортируем класс формы, чтобы сослаться на неё во view-классе
# было from .forms import CreationForm , PasswordChangeView
# from django import forms

from django.contrib.auth.views import (LoginView, LogoutView,
                                       PasswordChangeDoneView,
                                       PasswordChangeView,
                                       PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetDoneView)
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CreationForm


class LoginView:
    value = "{{csrf_token}}"
    # success_url = reverse_lazy('posts:posts')
    template_name = 'users/login.html'


class LogoutView:
    template_name = 'users/logged_out.html'


class SignUp(CreateView):
    form_class = CreationForm
    # После успешной регистрации перенаправляем пользователя на главную.
    success_url = reverse_lazy('users:login')
    template_name = 'users/signup.html'


class PasswordResetView:
    success_url = reverse_lazy('users:password_reset_done')
    template_name = 'users/password_reset_form.html'


class PasswordResetDoneView:
    # success_url = reverse_lazy('posts:posts')
    template_name = 'users/password_reset_done.html'


class PasswordResetConfirmView:
    success_url = 'users/password_reset_done.html'
    template_name = 'users/password_reset_confirm.html'


class PasswordResetCompleteView:
    template_name = 'users/password_reset_complete.html'


class PasswordChangeView:
    success_url = reverse_lazy('users/password_change_done.html')
    template_name = 'users/password_change_form.html'


class PasswordChangeDoneView:
    template_name = 'users/password_change_done'
