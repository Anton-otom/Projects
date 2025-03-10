from allauth.account.forms import LoginForm, SignupForm, PasswordField
from django import forms


# Кастомизация формы из модуля allauth для входа в систему
class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["login"] = forms.CharField(label="Имя пользователя или e-mail")
        self.fields['login'].widget.attrs.update({'placeholder': ''})
        self.fields["password"].widget = forms.PasswordInput(
            attrs={'label': "Пароль", 'autocomplete': 'new-password', 'placeholder': ''}
        )
        self.fields["remember"] = forms.BooleanField(label="Запомнить", required=False)


# Кастомизация формы из модуля allauth для регистрации нового пользователя
class CustomSignupForm(SignupForm):
    first_name = forms.CharField(label="Имя", required=True)
    last_name = forms.CharField(label="Фамилия")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'placeholder': ''})
        self.fields["username"] = forms.CharField(label="Имя пользователя")
        self.fields['username'].widget.attrs.update({'placeholder': ''})
        self.fields["password1"].widget = forms.PasswordInput(
            attrs={'label': "Пароль", 'autocomplete': 'new-password', 'placeholder': ''}
        )
        self.fields["password2"].widget = forms.PasswordInput(
            attrs={'label': "Пароль (ещё раз)", 'autocomplete': 'new-password', 'placeholder': ''}
        )
