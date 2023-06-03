import json
from pprint import pprint


def movie_info(movie, genres):
    genres_names = []
    gerne_ids = movie['genre_ids']
    for genre_id in gerne_ids:
        for genre in genres:
            if genre['id'] == genre_id:
                genres_names.append(genre['name'])
    
    result = {
        'id': movie['id'],
        'title': movie['title'],
        'poster_path': movie['poster_path'],
        'vote_average': movie['vote_average'],
        'overview': movie['overview'],
        'genres_names': genres_names
    }
    return result
        

# 아래의 코드는 수정하지 않습니다.
if __name__ == '__main__':
    movie_json = open('data/movie.json', encoding='utf-8')
    movie = json.load(movie_json)

    genres_json = open('data/genres.json', encoding='utf-8')
    genres_list = json.load(genres_json)

    pprint(movie_info(movie, genres_list))
