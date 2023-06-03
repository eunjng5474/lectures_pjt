# requests 사용 예시 2

import requests
from pprint import pprint

URL = 'https://api.themoviedb.org/3/movie/popular'

params = {
    'api_key': '439176298e4e775453299517d3d9e644',
    'language': 'ko-KR',
}

response = requests.get(URL, params=params).json()
pprint(response['results'])
