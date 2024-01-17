from typing import Any
from .models import Post
from django import forms
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'image' , 'category')

        widgets = {
            'title' : forms.TextInput(attrs={'class': 'input'}),
            'content' : forms.Textarea(attrs={'class': 'textarea' , 'rows': 10}),
            'image' : forms.FileInput(attrs={'class': 'input'}),
            'category': forms.Select(),
        }
        
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if Post.objects.filter(title=title).exists():
            raise forms.ValidationError('Title is already exits')
        return title