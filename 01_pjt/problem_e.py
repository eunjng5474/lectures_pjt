import json


def dec_movies(movies):
    # 여기에 코드를 작성합니다.  
    result = []
    for movie in movies:
        movies_detail = json.load(open(f'data/movies/{movie["id"]}.json', encoding='utf-8'))
        if movies_detail['release_date'][5:7] == '12':
            result.append(movies_detail['title'])
    return result


# 아래의 코드는 수정하지 않습니다.
if __name__ == '__main__':
    movies_json = open('data/movies.json', encoding='utf-8')
    movies_list = json.load(movies_json)
    
    print(dec_movies(movies_list))
