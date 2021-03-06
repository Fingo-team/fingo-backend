import time
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from movie.models import BoxofficeRank
from utils.movie import searchMixin


def get_boxoffice_moviename():
    today = datetime.now().strftime("%Y%m%d")
    boxoffice_url = "http://movie.daum.net/boxoffice/weekly?" \
                    "startDate={date}".format(date=today)

    r = requests.get(boxoffice_url)
    bs = BeautifulSoup(r.text, "html.parser")

    movie_list = bs.select(".tit_join > a")

    movie_names = [
        movie.text
        for movie in movie_list
    ]

    return movie_names


def create_boxoffice(rank, movie):
    BoxofficeRank.objects.create(rank=rank, movie=movie)


def init_boxoffice():
    movie_arr = get_boxoffice_moviename()
    boxoffice_list = []

    for movie in movie_arr:
        time.sleep(1)
        boxoffice_list.append(searchMixin.search_movie(movie, boxoffice=True))

    BoxofficeRank.objects.all().delete()
    for rank, movie in enumerate(boxoffice_list):
        create_boxoffice(rank=rank+1, movie=movie)


class Command(BaseCommand):
    def handle(self, *args, **options):
        init_boxoffice()
