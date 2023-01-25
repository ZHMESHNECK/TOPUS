from django import forms
from .models import *
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from captcha.fields import CaptchaField


class AddPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = 'Категория не выбрана'

    class Meta:
        model = Tank
        # fields = '__all__' # добавить все поля кроме автоматических
        fields = ['title', 'slug', 'content', 'photo', 'cat']
        widgets = {'title': forms.TextInput(attrs={'class': 'form-input'}),
                   'content': forms.Textarea(attrs={'cols': 60, 'rows': 10})}

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 200:
            raise ValidationError('Длина превышает 200 символов')

        return title


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model=User
        fields=('username', 'email','password1', 'password2')


# class AddressForm(forms.ModelForm):
#     username = forms.CharField(
#         min_length=5, label='Логин', widget=forms.TextInput())
#     email = forms.CharField(label='Почта', widget=forms.TextInput())
#     password1 = forms.CharField(
#         min_length=8, label='Пароль', widget=forms.PasswordInput())
#     password2 = forms.CharField(
#         min_length=8, label='Повтор пароля', widget=forms.PasswordInput())

#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password1', 'password2')

#     def clean_password2(self):
#         cd = self.cleaned_data
#         if cd['password1'] != cd['password2']:
#             raise forms.ValidationError('Пароли не совпадают')
#         return cd['password2']


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput())
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=100)
    email = forms.EmailField(label='Почта')
    content = forms.CharField(label='Текст',
        widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
    captcha = CaptchaField()


class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ('name','email','text')
        
class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(max_length=100)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    status = forms.BooleanField(required=False)
    
    class Meta:
        model = Profile
        fields = ['image','status']