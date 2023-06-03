from django import forms
from .models import Movie

class MovieForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(MovieForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
				'class': 'txt-width'
				})
    class Meta:
        model = Movie
        fields = '__all__'