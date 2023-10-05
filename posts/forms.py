from django import forms
from posts.models import Post


class PostForm(forms.ModelForm):
  title = forms.CharField(label='title')
  content = forms.CharField(
    label='content',
    widget=forms.Textarea(attrs={'rows': 10, 'cols': 30})
	)
  
  class Meta:
    model = Post
    fields = ('title', 'content',)