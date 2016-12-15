from django.conf import settings
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json

from movie.models import Actor, StillCut, Movie, Director, MovieActorDetail, Genre, Nation


def get_actor_director(url):
    r = requests.get(url)
    movie_detail_page = BeautifulSoup(r.text, "html.parser")
    appear_list = movie_detail_page.select("ul.list_join.list_staff > li")

    actor_arr = []
    director_arr = []

    for appear in appear_list:
        ret_dic = {}

        ret_dic["daum_id"] = appear.select("a")[0]["href"].split("=")[1]
        img_url = appear.select("img")[0]
        ret_dic["name"] = img_url["alt"]
        ret_dic["img"] = img_url["src"]
        ret_dic["role"] = appear.select("span.txt_join")[0].text
        if ret_dic["role"] == "감독":
            director_arr.append(ret_dic)
        else:
            actor_arr.append(ret_dic)

    return {"actors": actor_arr,
            "directors": director_arr}


def insert_db(movie_name):
    req = "https://apis.daum.net/contents/movie?apikey={apikey}" \
          "&output=json&q={movie_name}".format(apikey=settings.DAUM_API_KEY,
                                               movie_name=movie_name)
    res = requests.get(req)

    res_dic = json.loads(res.text)

    return create_movie_object(res_dic=res_dic)


def create_movie_object(res_dic):
    if res_dic.get("channel") is not None and len(res_dic["channel"]["item"]) != 0:
        movie_url = res_dic["channel"]["item"][0]["story"][0]["link"]
        daum_code = movie_url.split("=")[1]

        movie = None

        try:
            movie = Movie.objects.get(daum_code=daum_code)
        except:
            title = res_dic["channel"]["item"][0]["title"][0]["content"]
            #genre = res_dic["channel"]["item"][0]["genre"][0]["content"]
            story = res_dic["channel"]["item"][0]["story"][0]["content"]
            movie_img = res_dic["channel"]["item"][0]["thumbnail"][0]["content"]
            first_run_date = res_dic["channel"]["item"][0]["open_info"][0]["content"]
            #nation = res_dic["channel"]["item"][0]["nation"][0]["content"]
            nations = res_dic["channel"]["item"][0]["nation"]
            genres = res_dic["channel"]["item"][0]["genre"]
            to_date = datetime.strptime(first_run_date.replace(".", "-"), "%Y-%m-%d")

            appear_dic = get_actor_director(movie_url)

            director_arr = [
                Director.objects.get_or_create(daum_code=director["daum_id"],
                                               defaults={
                                                   "name": director["name"],
                                                   "img": director["img"]})[0]
                for director in appear_dic["directors"]
            ]

            actor_arr = [
                {"actor": Actor.objects.get_or_create(daum_code=actor["daum_id"],
                                                      defaults={
                                                          "name": actor["name"],
                                                          "img": actor["img"]})[0],
                 "role": actor["role"]}
                for actor in appear_dic["actors"]
            ]
            genre_arr = [
                Genre.objects.get_or_create(name=genre["content"])[0]
                for genre in genres
            ]

            nation_arr = [
                Nation.objects.get_or_create(name=nation["content"])[0]
                for nation in nations
            ]

            # movie = Movie(daum_code=daum_code,
            #               title=title,
            #               genre=genre,
            #               story=story,
            #               img=movie_img,
            #               first_run_date=to_date,
            #               nation_code=nation)
            movie = Movie(daum_code=daum_code,
                          title=title,
                          story=story,
                          img=movie_img,
                          first_run_date=to_date,
                          )

            # from IPython import embed; embed()
            movie.save()

            movie.director.add(*director_arr)
            movie.genre.add(*genre_arr)
            movie.nation_code.add(*nation_arr)

            stillcut_list = [
                res_dic["channel"]["item"][0]["photo"+str(i)]["content"].split("=")[1].replace("%3A", ":").replace("%2F","/")
                for i in range(1, 6)
            ]

            for img in stillcut_list:
                StillCut.objects.get_or_create(img=img,
                                               movie=movie)

            for actor in actor_arr:
                MovieActorDetail.objects.get_or_create(actor=actor["actor"],
                                                       movie=movie,
                                                       defaults={
                                                           "role": actor["role"]
                                                       })
        finally:
            return movie
    else:
        pass
