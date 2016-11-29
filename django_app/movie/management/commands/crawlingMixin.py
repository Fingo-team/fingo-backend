from django.conf import settings
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json

from movie.models import Actor, StillCut, Movie, Director, MovieActorDetail


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


def get_stillcuts(naver_code):
    url = "http://movie.naver.com/movie/bi/mi/photoView.nhn?" \
          "code={code}".format(code=naver_code)

    r = requests.get(url)
    bs = BeautifulSoup(r.text, "html.parser")

    parsing_target = bs.select("li._list")[:5]

    target_list = [
        json.loads(target["data-json"])
        for target in parsing_target
        ]

    stillcutt_list = [
        target["fullImageUrl886px"]
        for target in target_list
        ]

    return stillcutt_list


def insert_db(movie_names):
    naver_code = movie_names[0]
    movie_name = movie_names[1]

    req = "https://apis.daum.net/contents/movie?apikey={apikey}" \
          "&output=json&q={movie_name}".format(apikey=settings.DAUM_API_KEY,
                                               movie_name=movie_name)
    res = requests.get(req)

    res_dic = json.loads(res.text)

    return create_movie_object(res_dic=res_dic,
                               naver_code=naver_code)


def create_movie_object(res_dic, naver_code):
    if res_dic.get("channel") is not None and len(res_dic["channel"]["item"]) != 0:
        movie_url = res_dic["channel"]["item"][0]["story"][0]["link"]
        daum_code = movie_url.split("=")[1]

        movie = None

        try:
            movie = Movie.objects.get(daum_code=daum_code)
        except:
            title = res_dic["channel"]["item"][0]["title"][0]["content"]
            genre = res_dic["channel"]["item"][0]["genre"][0]["content"]
            story = res_dic["channel"]["item"][0]["story"][0]["content"]
            movie_img = res_dic["channel"]["item"][0]["thumbnail"][0]["content"]
            first_run_date = res_dic["channel"]["item"][0]["open_info"][0]["content"]
            nation = res_dic["channel"]["item"][0]["nation"][0]["content"]
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

            movie = Movie(naver_code=naver_code,
                          daum_code=daum_code,
                          title=title,
                          genre=genre,
                          story=story,
                          img=movie_img,
                          first_run_date=to_date,
                          nation_code=nation)
            # from IPython import embed; embed()
            movie.save()

            movie.director.add(*director_arr)

            stillcut_list = get_stillcuts(naver_code)
            for img in stillcut_list:
                StillCut.objects.get_or_create(img=img,
                                               defaults={
                                                   "movie": movie
                                               })

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
