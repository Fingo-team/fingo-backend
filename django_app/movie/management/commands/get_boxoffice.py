from django.core.management.base import BaseCommand
from movie.management.commands import crawlingMixin
import time
import requests
from bs4 import BeautifulSoup
from movie.models import BoxofficeRank


def get_boxoffice_moviename():
    boxoffice_url = "http://movie.naver.com/movie/sdb/rank/rboxoffice.nhn"

    r = requests.get(boxoffice_url)
    bs = BeautifulSoup(r.text, "html.parser")

    movie_list = bs.select("div.tit1 > a")

    movie_names = [
        (movie["href"].split("=")[1], movie.text)
        for movie in movie_list
    ]

    return movie_names


def create_boxoffice(rank, movie):
    BoxofficeRank.objects.create(rank=rank, movie=movie)


def init_boxoffice():
    movie_arr = get_boxoffice_moviename()
    boxiffice_list = []

    for movie in movie_arr:
        time.sleep(1)
        boxiffice_list.append(crawlingMixin.insert_db(movie))

    BoxofficeRank.objects.all().delete()
    for rank, movie in enumerate(boxiffice_list):
        create_boxoffice(rank=rank+1, movie=movie)


class Command(BaseCommand):
    def handle(self, *args, **options):
        init_boxoffice()