from django import forms
from django.shortcuts import render, redirect
from posts.models import Post, Category


class PostForm(forms.Form):
    title = forms.CharField(max_length=255)
    content = forms.CharField(widget=forms.Textarea)
    image = forms.ImageField(required=False)
    #rate = forms.IntegerField(min_value=1, max_value=5)

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title == 'kosyak':
            raise forms.ValidationError("Недопустимое название поста!")
        return title
    
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) < 50:
            raise forms.ValidationError("Описание слишком короткое!")
        return content

class PostModelForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'category']


class CategoryModelForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title', 'description', 'is_active']

