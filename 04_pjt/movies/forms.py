from django import forms
from .models import Movie

class MovieForm(forms.ModelForm):
    # 장르 = forms.필드(위젯=forms.인풋(attr={'속성':값}))
    score = forms.FloatField(widget=forms.NumberInput(attrs={'step':0.5, 'min':0, 'max':5}))

    class Meta:
        model = Movie
        fields = '__all__'