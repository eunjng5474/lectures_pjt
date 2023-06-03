# DB를 활용한 웹 페이지 구현

## 프로젝트 목표

- 데이터를 생성, 조회, 수정, 삭제할 수 있는 Web application 제작
- Django web framework를 사용한 데이터 처리
- Django Model과 ORM에 대한 이해
- Djnago ModelForm을 활용한 사용자 요청 데이터 유효성 검증
- Django Static files 관리 및 image file 업로드

## Model

```python
class Movie(models.Model):
    national_choices = (
        ('comedy', 'comedy'),
        ('thriller', 'thriller'),
        ('romance', 'romance'),
    )

    title = models.CharField(max_length=20)
    audience = models.IntegerField()
    release_date = models.DateField()
    genre = models.CharField(max_length=30, choices=national_choices)
    score = models.FloatField()
    poster_url = models.CharField(max_length=50)
    description = models.TextField()
    actor_image = models.ImageField(blank=True, null=True)
```

[추가]
- Form에서 genre 필드에서 장르 데이터를 선택할 수 있도록 하기 위해서 class 내부에서 national_choices에서 튜플 형식으로 값을 주고, 이후 CharField()에서 `choices=national_choices` 방식으로 진행.

- ![](C:\Users\SSAFY\AppData\Roaming\marktext\images\2023-03-24-14-44-38-image.png)

- 이런식으로 장르 선택 가능하게 됨.

- CharField()는 max_length 필수이므로 주의

## Admin
- 모델 Movie를 Admin site에 등록
- `admin.site.register(Movie)` 추가

## base.html
- 화면 상단에 header.jpg 고정
- ```html
  {% load static %}
  ...

  <body>
    <img src="{% static 'header.jpg' %}" alt="">
    
    {% block content %}
    {% endblock content %}
  </body>
  ```
- base.html 상단에 `load static` 꼭 추가하기

### 이미지 넣을 때
- setting.py
```python
STATIC_URL = '/static/'
STATICFILES_DIRS=[
    BASE_DIR / 'static',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

- mypjt/urls.py
```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('movies/', include('movies.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

## CRUD
- movies/urls.py
```python
from . import views

app_name = 'movies'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:movie_pk>/', views.detail, name='detail'),
    path('create/', views.create, name='create'),
    path('<int:movie_pk>/update/', views.update, name='update'),
    path('<int:movie_pk>/delete/', views.delete, name='delete'),
]
```
  - 이 때 pk값 필요한 경우 `<int:movie_pk>/` 추가 잊지 않기

- views에서 form 사용을 위해 movies에 forms.py 생성
```python
from django import forms
from .models import Movie

class MovieForm(forms.ModelForm):
    # 장르 = forms.필드(위젯=forms.인풋(attr={'속성':값}))
    score = forms.FloatField(widget=forms.NumberInput(attrs={'step':0.5, 'min':0, 'max':5}))

    class Meta:
        model = Movie
        fields = '__all__'
```
- models.py의 Movie import하고, MovieForm 만들기
- score는 input element attribute 설정


- movies/views.py
```python
from django.shortcuts import render, redirect
from .models import Movie
from .forms import MovieForm
from django.views.decorators.http import require_http_methods, require_POST
```

## INDEX
- views.py
```python
def index(request):
    movies = Movie.objects.all()
    context = {'movies':movies}
    return render(request, 'movies/index.html', context)
```

- index.html
```html
{% extends 'base.html' %}

{% block content %}
  <h1>INDEX</h1>
  <a href="{% url 'movies:create' %}">CREATE</a>
  <hr>

  {% for movie in movies %}
    <p><a href="{% url 'movies:detail' movie.pk %}">{{movie.title}}</a></p>
    <p>{{movie.score}}</p>
  {% endfor %}
{% endblock content %}
```
  - title 누르면 detail 페이지로 이동. 이 때 detail은 pk값 필요하므로 url 태그에 같이 써주기!


## DETAIL
- views.py
```python
def detail(request, movie_pk):
    movie = Movie.objects.get(pk=movie_pk)
    context = {'movie':movie}
    return render(request, 'movies/detail.html', context)

# POST일 때맏 delete
@require_POST
def delete(request, movie_pk):
    movie = Movie.objects.get(pk=movie_pk)
    movie.delete()
    return redirect('movies:index')
```

- detail.html
```html
    ...
    # if문 써서 actor_image 있는 경우에만 보이도록 설정
    # 이 때 actor_image는 작성자가 첨부하는 사진
    {% if movie.actor_image %}
      <p>Actor: </p>
      <img src="{{movie.actor_image.url}}" alt="">
    {% endif %}
    <p>{{movie.description}}</p>

  # update 페이지로 가는 링크
  <a href="{% url 'movies:update' movie.pk%}">UPDATE</a>

  # delete 버튼 추가해서 삭제 가능하도록
  # POST 방식으로만 삭제 가능하게 하기 위해 method="POST", csrt_token
  # 별도 html 생성이 아닌 detail.html에서 추가해서 삭제되도록
  <form action="{% url 'movies:delete' movie.pk%}" method="POST" id="delete-form">
    {% csrf_token %}
    <input type="submit" value="DELETE" id="delete-btn">
  </form>
```



## CREATE
- views.py
```python
@require_http_methods(['GET', 'POST'])
def create(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save()
            return redirect('movies:detail', movie.pk)
    else:
        form = MovieForm()

    context = {'form': form}
    return render(request, 'movies/create.html', context)
```
  - create는 GET, POST 방식 둘 다 가능하도록 데코레이터 사용
  - POST일 때는 request값 추가한 MovieForm, 유효성 검사해서 통과하면 detail 페이지로 가도록 redirect
  - 이 때 detail 페이지는 pk값 필요 
  - GET 방식일 때는 `MovieFrom()`

- create.html
```html
  <form action="{% url 'movies:create' %}" method="POST" enctype="multipart/form-data">
    {% csrf_token %}
    {{form.as_p}}
    <input type="submit" value="Submit">
  </form>
```
- POST방식
- 파일 첨부 위해 `enctype="multipart/form-data"`


## UPDATE
- views.py
```python

@require_http_methods(['GET', 'POST'])
def update(request, movie_pk):
    movie = Movie.objects.get(pk=movie_pk)

    if request.method == "POST":
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('movies:detail', movie_pk=movie.pk)
    else:
        form = MovieForm(instance=movie)

    context = {
        'form':form,
        'movie':movie
        }
    return render(request, 'movies/update.html', context)
```

- create와 비슷하지만 update에서는 첨부한 파일 가져와야 하기 때문에 `instance=movie` 추가