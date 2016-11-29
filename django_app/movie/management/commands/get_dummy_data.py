from django.core.management.base import BaseCommand
from movie.management.commands import crawlingMixin
import requests
import time
from datetime import datetime
from bs4 import BeautifulSoup


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
        for page_num in range(1, 5)
        ]

    for page_num in range(len(movie_arr)):
        time.sleep(10)
        for cnt, movie in enumerate(movie_arr[page_num]):
            if cnt != 0 and cnt % 10 == 0:
                time.sleep(10)
            crawlingMixin.insert_db(movie)
            time.sleep(1)


class Command(BaseCommand):
    def handle(self, *args, **options):
        init_naver_movie()