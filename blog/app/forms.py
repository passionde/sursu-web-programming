"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _

from app.models import Comment, Blog


class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254, widget=forms.TextInput({
        'class': 'form-control',
        'placeholder': 'Логин'
    }))
    password = forms.CharField(label=("Password"), widget=forms.PasswordInput({
        'class': 'form-control',
        'placeholder': 'Пароль'
    }))


class AnketaForm(forms.Form):
    name = forms.CharField(label='Baшe имя', min_length=2, max_length=100)
    city = forms.CharField(label='Baш гоpод', min_length=2, max_length=100)
    job = forms.CharField(label='Ваш род занятий', min_length=2, max_length=100)
    gender = forms.ChoiceField(label='Baш noл', choices=[('1', 'Мужской'), ('2', 'Женский')], widget=forms.RadioSelect,
                               initial=1)
    internet = forms.ChoiceField(
        label='Bы пользуетесь интернетом',
        choices=(
            ('1', 'Каждый день'),
            ('2', 'Несколько раз в день'),
            ('3', 'Несколько раз в неделю'),
            ('4', 'Несколько раз в месяц')),
        initial=1
    )
    notice = forms.BooleanField(label='Получать новости сайта нa e-mail?', required=False)
    email = forms.EmailField(label='Baш e-mail', min_length=7)
    message = forms.CharField(label='Kopoтко o ceбe', widget=forms.Textarea(attrs={'rows': 12, 'cols': 20}))


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment  # используемая модель
        fields = ('text',)  # требуется заполнить только поле text
        labels = {'text': "Комментарий"}  # метка к полю формы text


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'description', 'content', 'image',)
        labels = {
            'title': 'Заголовок',
            'description': 'Краткое содержание',
            'content': 'Полное содержание',
            'image': 'Картинка'
        }
