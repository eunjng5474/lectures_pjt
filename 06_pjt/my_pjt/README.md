# 관계형 데이터베이스 설계
## 프로젝트 목표
- 데이터를 생성, 조회, 수정, 삭제할 수 있는 Web application 제작
- Django web framework를 사용한 데이터 처리
- Django Model과 ORM에 대한 이해
- Django Authentication System에 대한 이해
- Database many to one relationship(1:N) 및 many to many relationship(M:N)에 대한 이해

### base
- `$ django-admin startproject mypjt .`으로 프로젝트 생성
- `$ python manage.py startapp app_name`으로 movies, accounts 어플리케이션 생성 
- mypjt/settings.py에 apps 추가, templates에 `[BASE_DIR/ 'templates']` 추가해서 base.html있는 templates 폴더 찾아갈 수 있도록 하기 
- `AUTH_USER_MODEL = 'accounts.User'` 
- static, media url 및 dir 추가하기 
- mypjt/ulrs.py에 movies, accounts url 추가 및 static 추가

- base.html 템플릿 만들기
- nav 태그 사용해서 상단 네비게이션 바 만들기
- `{% if user.is_authenticated %}`를 통해 로그인, 비로그인 상태에 따라 다른 링크 출력
- static 폴더 생성해서 base.css, base.js를 통해 참조 가능하도록 만들기 


## Accounts

### accounts/models.py
```python
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')
```
- `models.ManyToManyField`를 통해 user_followings 중개 테이블 생성
- 내가 상대방을 팔로우한다고 해서 상대방도 나를 자동으로 팔로우하지 않도록 하기 위해 `symmetrical=False`
- `related_name`
  - target model이 source model을 참조할 때 사용할 manager name
  - ForeignKey의 related_name과 동일
- model update후에는 migrations 진행하기!!


### accounts/forms.py
```python
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        
class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = ('first_name', 'last_name',)
```
- 회원가입, 회원 정보 수정 form 정의


### accounts/urls.py
```python
from django.urls import path
from . import views

app_name='accounts'

urlpatterns = [
  # ...
  # login, logout, signup, delete, update, password
  path('profile/<str:username>/', views.profile, name='profile'),
  path('<int:user_pk>/follow/', views.follow, name='follow'),
]
```
- username을 통해 profile 페이지로 이동
- user_pk를 통해 follow 구현 


### accounts/views.py
```python
  # ...
  @require_safe
  def profile(request, username):
      user = get_object_or_404(get_user_model(), username=username)
      context = {
          'user': user
      }
      return render(request, 'accounts/profile.html', context)

  @require_POST
  def follow(request, user_pk):
      if request.user.is_authenticated:
          person = get_object_or_404(get_user_model(), pk=user_pk)
          if request.user in person.followers.all():
              person.followers.remove(request.user)
          else:
              person.followers.add(request.user)
          return redirect('accounts:profile', person.username)
      else:
          return redirect('accounts:login')

```
- `get_object_or_404`를 통해서 정확한 정보 입력하지 않을 시 404 페이지 보여주도록
- profile
  - username을 통해 해당 user정보 가져와서 profile.html로 가도록 
- follow
  - follower한 user라면 followers에서 remove하여 언팔로우 할 수 있도록,
  - 아니라면 followers.add를 통해 팔로우 할 수 있도록 하기
  - login한 회원 아니면 로그인 하도록 login페이지로 redirect


### accounts/profile.html
- `{{user.following.count}}`를 통해 팔로잉 수 count해서 보여주기
- `{% if request.user != user %}`를 통해 request.user와 user가 다를 때만 팔로우/언팔로우 버튼 보여주기 

- `{% for movie in user.movie_set.all %}`을 통해 user의 작성글 보여주기
- href 연결해서 자세히 보기 버튼 클릭 시 해당 글로 이동 

- `{% for comment in user.comment_set.all %}`을 통해 user의 작성 댓글 보여주기
- `{% for movie in user.like_movies.all %}`을 통해 user가 좋아요한 게시글 보여주기



## Movies
### movies/models.py

```python
  from django.db import models
  from django.conf import settings

  # Create your models here.
  class Movie(models.Model):
      title = models.CharField(max_length=20)
      description = models.TextField()
      user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
      like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_movies')
      dislike_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='dislike_movies')
      
      
  class Comment(models.Model):
      user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
      movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
      content = models.CharField(max_length=100)
```
- Movie
  - foreignkey를 통해 외부 키(user) 참조
    - 이 때 `from django.conf import settings` 한 후 `settings.AUTH_USER_MODEL`을 통해 settings.py에서 설정한 user 가져오기
  - 중개 테이블 생성해서 좋아요, 싫어요 구현

- Comment
  - 외래키 참조. `on_delete=models.CASCADE`를 통해 부모 객체가 삭제됐을 때 이를 참조하는 객체도 삭제되도록 하기


### movies/forms.py
```python
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
```
- models에서 정의한 모델 가져오기
- exclude를 통해 form에서 보여주지 않을 필드 제시 


### accounts/urls.py
```python
  from django.urls import path
  from . import views

  app_name = 'movies'
  urlpatterns = [
    # '', create, <int:pk>, <pk>/update, <pk>/delete 
    path('<int:pk>/comments/', views.comment_create, name='comment_create'),
    path('<int:movie_pk>/comments/<int:comment_pk>/delete/', views.comment_delete, name='comment_delete'),
    path('<int:movie_pk>/likes/', views.likes, name='likes'),
    path('<int:movie_pk>/dislikes/', views.dislikes, name='dislikes'),
  ]
```
- 댓글 달기, 댓글 삭제, 좋아요, 싫어요
  - 댓글 삭제 시에는 해당 글(movie_pk)과 댓글의 pk값(comment_pk) 모두 필요


### accounts/views.py
```python
  @require_http_methods(['GET', 'POST'])
  def create(request):
      if request.user.is_authenticated:
          if request.method == 'POST':
              form = MovieForm(request.POST, request.FILES)
              if form.is_valid():
                  movie = form.save(commit=False)
                  movie.user = request.user
                  movie.save()
                  return redirect('movies:detail', movie.pk)
          else:
              form = MovieForm()
          
          context = {'form': form}
          return render(request, 'movies/create.html', context)
      else:
          return redirect('movies:index')
    
```
- 로그인 한 회원만 글 작성 가능하도록 하기
- `save(commit=False)`
  - 아직 데이터베이스에 저장되지 않은 인스턴스를 반환
  - 저장하기 전에 객체에 대한 사용자 지정 처리를 수행할 때 유용하게 사용
  - 즉, save 메서드의 commit 옵션을 통해 DB에 저장되기 전에 movie 객체 저장하기

```python
  @require_safe
  def detail(request, pk):
      movie = Movie.objects.get(pk=pk)
      comment_form = CommentForm()
      comments = movie.comment_set.all()
      context = {
          'movie':movie,
          'comment_form': comment_form,
          'comments': comments,
      }
      return render(request, 'movies/detail.html', context)
```
- 댓글 기능을 제공하므로 detail에서 comment에 대한 내용도 context에 담기

```python
  @require_POST
  def comment_create(request, pk):
      if not request.user.is_authenticated:
          return redirect('accounts:login')

      movie = Movie.objects.get(pk=pk)
      comment_form = CommentForm(request.POST)
      if comment_form.is_valid():
          comment = comment_form.save(commit=False)
          comment.movie = movie
          comment.user = request.user
          comment.save()
      return redirect('movies:detail', movie.pk)
```
- pk값을 통해 해당 글 정보 가져오고, comment form의 유효성 검사 후 DB 저장되기 전에 comment 객체 저장
  - comment의 user는 request.user

```python
  @require_POST
  def comment_delete(request, movie_pk, comment_pk):
      if not request.user.is_authenticated:
          return redirect('accounts:login')
      comment = Comment.objects.get(pk=comment_pk)
      if request.user == comment.user:
          comment.delete()
      return redirect('movies:detail', movie_pk)
```
- 댓글 삭제 시에는 movie(글), comment(댓글)의 pk값 모두 필요 

```python
  @require_POST
  def likes(request, movie_pk):
      if request.user.is_authenticated:
          movie = Movie.objects.get(pk=movie_pk)
          if movie.like_users.filter(pk=request.user.pk).exists():
              movie.like_users.remove(request.user)
          else:
              movie.like_users.add(request.user)
          return redirect('movies:index')
      return redirect('accounts:login')
```
- follow와 마찬가지로 이미 좋아요 한 경우 좋아요 취소를, 아닌 경우 좋아요를 할 수 있도록


### accounts/detail.html
- `{% for comment in comments %}`를 통해 댓글 보여주기
  - request.user와 comment.user가 일치할 경우에만 삭제 가능하도록 삭제 버튼 보여주기 
  - `{% empty %}`를 통해 댓글 존재하지 않을 경우 '댓글이 존재하지 않습니다' 보여주기 
- comment_create, comment_form을 통해 댓글 작성 가능하도록 하기

### accounts/index.html
- 좋아요/싫어요 구현
  - 이 때 좋아요 form 내에 싫어요 작성하지 않도록 주의하기 => 이 경우 싫어요 눌러도 좋아요 누른 걸로 됨


