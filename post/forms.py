from django import forms
from django.forms import ModelForm
from .models import Comment


class PostCommentForm(ModelForm):
    body = forms.CharField(
        label="comment",
        widget=forms.Textarea(
            attrs={
                'name': 'comment',
                'class': 'form-control',
                'rows': "5",
                'placeholder': "Join the discussion and leave a comment!"
            })
    )

    class Meta:
        model = Comment
        fields = ('body',)
