from comments.models import Comment
from django import forms


class CommentForm(forms.ModelForm):
  content = forms.CharField(
    label='content',
    widget=forms.Textarea(attrs={'rows': 5, 'cols': 40})
	)
  
  class Meta:
    model = Comment
    fields = ('content',)