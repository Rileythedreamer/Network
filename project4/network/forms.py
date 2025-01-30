from django import forms
from django.forms import ModelForm

from .models import Post

#creating forms from models
    #post form
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'write something...',
                'rows': 8,
            }),
        }
        labels = {
            'content':'',
        }