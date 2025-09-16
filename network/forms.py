from django.forms import ModelForm
from django import forms
from .models import Post

class PostForm(ModelForm):
    class Meta:
        model = Post
        
        fields = ["content"]
        labels = {
            "content" : ""
        }
        widgets = {
            "content" : forms.Textarea(attrs = {
                "rows" : "3",
                "class" : "form-control w-75"
            })
        }