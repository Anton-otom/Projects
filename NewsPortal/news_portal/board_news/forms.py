from django import forms
from django.core.exceptions import ValidationError

from .models import Post


class PostForm(forms.ModelForm):
    text = forms.CharField(min_length=20)

    class Meta:
        model = Post
        fields = [
            'type_post',
            'categories',
            'title',
            'text',
        ]

    # def clean(self):
    #     cleaned_data = super().clean()
    #
    #     description = cleaned_data.get("description")
    #     name = cleaned_data.get("name")
    #
    #     if name == description:
    #         raise ValidationError(
    #             "Описание не должно быть идентичным названию."
    #         )
    #     return cleaned_data