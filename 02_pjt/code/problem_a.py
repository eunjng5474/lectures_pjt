import requests


def popular_count():
    # URL -> 내가 요청을 보내고자 하는 각 기능별 페이지의 주소
    # 1번 문제의 경우 popular (인기순 영화 목록을 적절한 요구사항에 맞게 요청을 보내면 응답해준다.)
    URL = 'https://api.themoviedb.org/3/movie/popular'

    # Query String Parameter -> API에서 제공해주는 각 기능별 페이지에서 요구하는 요청 방식에 맞춰서 작성한다.
        # ex) 네이버에서 검색창에 ssafy를 입력하면 주소창이 아래와 같이 나오는데
        # https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=ssafy
            # 이 중, search.naver? 뒷부분중 query 부분만 남기고 모두 지우면 아래와 같은 형태가 된다.
            # https://search.naver.com/search.naver?query=ssafy
            # 네이버는 위의 주소로, `?` 뒤에 query 라는 key에 어떠한 value를 집어넣으면 그 값을 검색한 결과를 보여준다.
            # 주소창에서 query 뒷부분만 다른 검색어로 바꿔서 결과 확인해보기

    # TMDB의 경우, 각 기능별로 Query String 혹은 Path Parameter 등 어떤 `키:벨류` 로 값을 보내주어야 하는지 페이지별로 기록되어 있다.
    # popular의 경우, `api_key` 라는 key에 TMDB 회원 가입 후 발급받은 토큰을 value로 담아 보내야 한다.
        # 그래서, `api_key` 에는 `string` (문자열 형태의) 토큰을 `required` 필수적으로 작성해 달라고 하고 있으며,
        # `language`, `age`, `region` 등은 `optional` 선택적으로 삽입가능하다.

    # 즉, TMDB에서 인기도순의 최신 영화 정보를 받아오려면 주소창에
    # 도메인 + Query String Parameter 를 적절히 요청하면된다.
        # 완성된 주소형태
        # https://api.themoviedb.org/3/movie/popular?api_key={TMDB_api_key}&language=ko-KR'
        # 여기서 &를 사용해 각자 다른 요구사항을 삽입할 수 있고,
        # language에 작성되는 내용은 국제 규격에 따라 대한민국의 한글을 표기하는 방법 ko-KR을 삽입해 준다.
    
    # 그래서 위와 같이 완성된 주소 전체를 requests에 넘겨주어도 되고,
    # requests를 사용하는 또 다른 방법으로 2번째 인자에
    # params 키워드 인자에 내가 직접 딕셔너리 형태로 요구사항을 작성한 뒤 요청을 보낼 수도 있다.

    # 주의할 점은 여기서도 key 값은 반드시 API 제공 사이트에서 제시하는 이름 그대로 작성할 것
        # ex) apikey: APIKEY: ApiKey: 등 TMDB가 말하는 api_key와 다른 형태면 안된다.
    params = {
        'api_key': '439176298e4e775453299517d3d9e644',
        'language': 'ko-KR'
    }

    # 그렇게 요청 보내 받아온 결과는 requests 타입의 데이터이고, # 파이썬에서 바로 쓸 수 없으며
    response = requests.get(URL, params=params) # <response [200]>

    # 파이썬에서 쓸 수 있도록 하기 위해 json() 메서드를 사용해
    # json 타입의 데이터를 파이썬의 자료형으로 변환한다.
    response = response.json() 
    '''
        {
            "page": 1,
            "results": [
                {
                "adult": false,
                ...
                "vote_count": 2746
                },
            ...
        }
    '''

    # 받아온 중첩 자료형을 잘 확인하여 문항에서 요구하는 바를 충족시키는 값을 반환한다.
    return len(response['results'])
    # 여기에 코드를 작성합니다.  


# 아래의 코드는 수정하지 않습니다.
if __name__ == '__main__':
    """
    popular 영화목록의 개수 반환
    """
    print(popular_count())
    # 20