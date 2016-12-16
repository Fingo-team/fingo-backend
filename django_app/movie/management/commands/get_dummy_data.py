import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand

from utils.movie import movieMixin


def get_all_moviename(page_num):
    url = "http://movie.naver.com/movie/sdb/rank/rmovie.nhn?" \
          "sel=pnt&date={date}6&page={page}".format(date=datetime.now().strftime("%Y%m%d"),
                                                    page=page_num)
    r = requests.get(url)
    bs = BeautifulSoup(r.text, "html.parser")

    movies = bs.select("div.tit5 > a")

    movie_names = [
        (movie["href"].split("=")[1], movie.text)
        for movie in movies
        ]

    return movie_names


def init_naver_movie():
    movie_arr = [
        get_all_moviename(page_num=page_num)
        for page_num in range(39, 40)
        ]

    for page_num in range(len(movie_arr)):
        time.sleep(10)
        for cnt, movie in enumerate(movie_arr[page_num]):
            if cnt != 0 and cnt % 10 == 0:
                time.sleep(1)
            movieMixin.search_movie(movie[1])
            time.sleep(1)


class Command(BaseCommand):
    def handle(self, *args, **options):
        init_naver_movie()
