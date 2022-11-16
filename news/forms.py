from django import forms
from django.core.exceptions import ValidationError
from .models import Post


class PostForm(forms.ModelForm):
   # text = forms.CharField(min_length=20)    # валидация по минимальному количеству

    class Meta:
        model = Post
        fields = [
            'category',
            'caption',
            'text',
            'author'
        ]

    def clean(self):
        cleaned_data = super().clean()
        caption = cleaned_data.get("caption")
        # if description is not None and len(description) < 20:
        #     raise ValidationError({
        #         "description": "Описание не может быть менее 20 символов."
        #     })

        text = cleaned_data.get("text")
        if caption == text:
            raise ValidationError("Заголовок не должно быть идентичен тексту.")

        return cleaned_data