import json


def max_revenue(movies):
    # 여기에 코드를 작성합니다.
    result = ''
    revenue = 0
    for movie in movies:
        movies_detail = json.load(open(f'data/movies/{movie["id"]}.json', encoding='utf-8'))
        if revenue <= movies_detail['revenue']:
            revenue = movies_detail['revenue']
            result = movies_detail['title']
    return result


        
        
# 아래의 코드는 수정하지 않습니다.
if __name__ == '__main__':
    movies_json = open('data/movies.json', encoding='utf-8')
    movies_list = json.load(movies_json)
    
    print(max_revenue(movies_list))
