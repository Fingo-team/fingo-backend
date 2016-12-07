__all__ = [
    'score_average',
]


def score_average(movie):
    movie_scores = movie.useractivity_set.all().exclude(score=None)
    try:
        movie_average = sum([movie_score.score for movie_score in movie_scores]) / len(movie_scores)
    except ZeroDivisionError:
        movie_average = 0
    movie.score = movie_average
    movie.save()
