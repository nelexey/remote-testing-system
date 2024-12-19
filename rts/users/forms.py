from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    name = forms.CharField(required=False)
    surname = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'name', 'surname', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Этот email уже используется.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.name = self.cleaned_data['name']
        user.surname = self.cleaned_data['surname']
        user.role = 'user'  # По умолчанию роль - обычный пользователь
        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя или Email')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Позволяем войти как по username, так и по email
        if '@' in username:
            try:
                user = User.objects.get(email=username)
                return user.username
            except User.DoesNotExist:
                raise forms.ValidationError('Неверный email или пароль')
        return username