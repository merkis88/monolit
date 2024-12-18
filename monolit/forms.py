from cProfile import label

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import modelformset_factory
from pyexpat.errors import messages

from .models import Profile, Post, AnswerOption

class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label="Пароль")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Повторите пароль")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': 'Логин',
            'email': 'Почта',
        }

    def clean(self):
        super().clean()
        pwd1 = self.cleaned_data.get('password1')
        pwd2 = self.cleaned_data.get('password2')
        if pwd1 and pwd2 and pwd1 != pwd2:
            raise ValidationError({"password2": ValidationError('Пароли не совпадают', code='password_mismatch')})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']
        labels ={
            'avatar': 'Фотография профиля'
        }

class UserUpdate(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {
            'username': 'Логин',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Почта'
        }

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exclude(id = self.instance.id).exists():
            raise forms.ValidationError("Это имя пользователя уже занято")
        return username

class ProfileUpdate(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']
        labels = {
            'avatar': 'Фотография профиля'
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'image', 'valid_duration']

class AnswerOptionForm(forms.ModelForm):
    class Meta:
        model = AnswerOption
        fields = ['text']

AnswerOptionFormSet = modelformset_factory(AnswerOption, form=AnswerOptionForm, extra=3)

