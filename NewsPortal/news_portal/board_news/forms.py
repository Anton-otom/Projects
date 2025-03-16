from django import forms
from django.core.exceptions import ValidationError
from django.forms import CheckboxSelectMultiple

from .models import Post


class PostForm(forms.ModelForm):
    text = forms.CharField(min_length=20, label="Текст")

    class Meta:
        model = Post
        fields = [
            'title',
            'categories',
            'text',
        ]
        labels = {
            'title': "Заголовок",
            'categories': "Категории",
        }
        widgets = {
            'categories': CheckboxSelectMultiple,
        }
        required = [
            'categories'
        ]

    def clean(self):
        cleaned_data = super().clean()

        text = cleaned_data.get("text")
        title = cleaned_data.get("title")

        if title == text:
            raise ValidationError(
                "Текст не должен быть идентичным заголовку."
            )
        return cleaned_data
