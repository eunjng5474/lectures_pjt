from django import forms
from .models import Movie, Comment

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        exclude = (
            'user',
            'like_users',
            'dislike_users',
        )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = (
            'article',
            'user',
            'movie',
            'parent',
        )


# class ReCommentForm(forms.ModelForm):
#     class Meta:
#         model = ReComment
#         fields = '__all__'
        