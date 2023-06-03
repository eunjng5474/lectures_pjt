from django import forms
from .models import Movie, Comment

class MovieForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(MovieForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
				'class': 'txt-width'
				})
    
    class Meta:
        model = Movie
        exclude = ('user', 'like_users', 'dislike_users',)
        
class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        exclude = ('movie', 'user',)