# 반응형 웹 페이지 구현

### 프로젝트 목표

- HTML을 통한 웹 페이지 마크업 이해

- CSS  라이브러리의 이해와 활용

- Bootstrap 컴포넌트 및 Grid system을 활용한 반응형 레이아웃 구성



### 01_nav_footer.html

#### Navigation Bar

- 스크롤 하더라도 화면 상단에 고정
  `class="sticky-top"`

- 메뉴 중 Login 클릭 시 modal component 나타나도록
  
  - nav-item 중 타입을 버튼으로 해서 modal 연결 버튼으로 만들기
  
  - 하단에 model 코드 따로 배치해서 modal 뜨도록 하기

```html
<li class="nav-item">
    <button type="button" class="btn nav-link" data-bs-toggle="modal" data-bs-target="#exampleModal">Login</button>
```

#### Footer

- 스크롤 해도 항상 화면 하단에 고정:

- 수직, 수평 가운데 정렬

```html
<footer class="container-fluid fixed-bottom text-center text-secondary-emphasis">
    <p>Web-bootstrap PJT, by Eunjeong</p>
</footer>
```



## 02_home.html

#### Header

- Bootstrap Carousel Component - carouselExampleAutoplaying 사용해서 이미지 3장이 자동으로 전환되도록

#### Section

```html
<div class="container text-center mx-auto">
        <div class="row">
          <div class="col">
            <div class="card mx-auto" style="width: 20rem;">
              <img src="images/movie1.jpg" class="card-img-top" alt="...">
              <div class="card-body">
                <h5 class="card-title">Card title</h5>
                <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>        
              </div>
            </div>
          </div>
```

- container, row로 묶은 뒤 col마다 card component로 구성해서 viewport크기에 따라 1~3개가 표시되도록



## 03_community.html

#### Aside(게시판 목록)

- `class="list-group col-12 col-lg-2"`을 통해 viewport 크기가 lg 이상일 때는 12칸 중 2칸만큼(1/6)의 너비 차지, lg 미만일 때는 12칸 차지

#### Section(게시판)

- lg 이상일 때만 보일 표를 생성한 후, aside와 flex로 묶어서 나란히 보이도록 설정

- `class="d-none d-lg-block col-lg-9"`을 통해 default는 보이지 않고, lg 이상일 때만 9칸 만큼 보이도록 설정

- `class="table table-striped"`, `thead class="table-dark"`를 통해 테마 설정

- lg 미만일 때 보이는 내용은 article 통해서 h1, h2, p태그 등으로 직접 작성

- 이를 ul 태그로 묶어서 `class="d-lg=none"`을 통해 lg 이상일 때 보이지 않도록 설정

#### Pagination

- bootstrap pagination component 사용

- `class="pagination justify-content-center"` 를 통해 수평 중앙 정렬
