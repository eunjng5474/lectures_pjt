# 사용자 인증 기반 DB 설계
## 프로젝트 목표
- 데이터를 생성, 조회, 수정, 삭제할 수 있는 Web application 제작
- Django web framework를 사용한 데이터 처리
- Django Model과 ORM에 대한 이해
- Django Authentication System에 대한 이해

### base
- base 템플릿 만들기
- bootstrap 사용
- base.css를 통해 기본 css 적용시키기
- java scripts 사용할 때 <script></script> 사이에 내용 적기
  - html에서 `onclick="function()"`을 통해서 클릭시 함수 실행되도록 


## Accounts
### accounts/models.py
- 모델 클래스의 이름 User, AbstractUser 모델 클래스 상속받기
```python
class User(AbstractUser):
    pass
```

### accounts/forms.py
```python
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = get_user_model()

class CustomUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = ('first_name', 'last_name',)
```



### accounts/urls.py
```python
app_name = 'accounts'
urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('delete/', views.delete, name='delete'),
    path('update/', views.update, name='update'),
    path('password/', views.change_password, name='change_password'),
]
```

### accounts/views.py
```python
@require_http_methods(['POST', 'GET'])
def login(request):
    if request.user.is_authenticated:
        return redirect('movies:index')
    else:
        if request.method == 'POST':
            form = AuthenticationForm(request, request.POST)
            if form.is_valid():
                auth_login(request, form.get_user())
                return redirect('movies:index')
        else:
            form = AuthenticationForm()

        context = {'form': form}
        return render(request, 'accounts/login.html', context)

@require_POST
def logout(request):
    auth_logout(request)
    return redirect('movies:index')

@require_http_methods(['POST', 'GET'])
def signup(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                auth_login(request, user)
                return redirect('movies:index')
        else:
            form = CustomUserCreationForm()
        context = {
            'form' : form,
        }
        return render(request, 'accounts/signup.html', context)
    else:
        return redirect('movies:index')

@require_POST
def delete(request):
    request.user.delete()
    auth_logout(request)
    return redirect('movies:index')

@require_http_methods(['POST', 'GET'])
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('movies:index')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form
    }
    return render(request, 'accounts/update.html', context)

@require_http_methods(['POST', 'GET'])
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('movies:index')
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form': form
    }
    return render(request, 'accounts/change_password.html', context)
```
- `if request.user.is_authenticated:`를 통해 로그인 유무에 따라 다르게 실행하기
  - 로그인 된 상태에서 로그인이나 회원가입 시도 시 불가능하도록 설정 
- `if form.is_valid():`를 통해 유효성 검사


### accounts/*.html
- `method="POST"`일 때 `csrf_token` 잊지 않기!


## Git branch
### branch
- 작업 공간을 나누어 독립적으로 작업할 수 있도록 도와주는 Git의 도구
- 원본에 대해 안전하다.
- 하나의 작업은 하나의 브랜치로 나누어 진행되므로 체계적인 개발이 가능하다.

- `git branch` : 로컬 저장소의 브랜치 목록 확인
- `git branch -r` : 원격 저장소의 브랜치 목록 확인
- `git branch branch_name` : 브랜치 생성
- `git branch -d branch_name` : 브랜치 삭제

- `git switch branch_name` : 브랜치로 이동
- `git merge branch_name` : merge

- `git push origin branch_name` : push

- branch 생성 -> switch -> 작업 -> push -> 원격저장소에서 `pull request` -> merge
