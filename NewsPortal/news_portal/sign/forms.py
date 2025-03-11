from allauth.account.forms import LoginForm, SignupForm, PasswordField
from django import forms
from django.contrib.auth.models import Group


# Кастомизация формы из модуля allauth для входа в систему
class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['login'] = forms.CharField(label='Имя пользователя или e-mail')
        self.fields['login'].widget.attrs.update({'placeholder': ''})

        self.fields['password'] = PasswordField(label='Пароль')
        self.fields['password'].widget.attrs.update({'placeholder': ''})

        self.fields['remember'] = forms.BooleanField(label='Запомнить', required=False)


# Кастомизация формы из модуля allauth для регистрации нового пользователя
class CustomSignupForm(SignupForm):
    first_name = forms.CharField(label='Имя', required=True)
    last_name = forms.CharField(label='Фамилия')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'placeholder': ''})

        self.fields['username'] = forms.CharField(label='Имя пользователя')
        self.fields['username'].widget.attrs.update({'placeholder': ''})

        self.fields['password1'] = PasswordField(label='Пароль')
        self.fields['password1'].widget.attrs.update({'placeholder': ''})

        self.fields['password2'] = PasswordField(label='Пароль (ещё раз)')
        self.fields['password2'].widget.attrs.update({'placeholder': ''})

    # Автоматическое добавление нового пользователя в группу "common"
    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user
