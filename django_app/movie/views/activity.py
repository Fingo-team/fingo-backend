from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from movie.models import Movie
from fingo_statistics.models import UserActivity
from fingo_statistics.serializations import UserCommentsSerializer, UserCommentCreateSerailizer
from utils.activity import average
from utils.statistics import count_all

__all__ = [
    "MovieAsUserComment",
    "MovieWish",
    "MovieScore"
]


# comment CRUD
class MovieAsUserComment(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserCommentCreateSerailizer
    queryset = UserActivity.objects.all()

    def get_object(self):
        user = self.request.auth.user
        movie = Movie.objects.get(pk=self.kwargs.get("pk"))
        instance = self.get_queryset().get(user=user, movie=movie)

        return instance

    def retrieve(self, request, *args, **kwargs):
        serial_data = UserCommentsSerializer(self.get_object())

        return Response(serial_data.data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        ua = self.get_object()
        serial = self.get_serializer(ua,
                                     data=request.data,
                                     partial=True)
        if serial.is_valid(raise_exception=True):
            serial.save()

        return Response(serial.data,
                        status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, *args, **kwargs):
        user_activity = self.get_object()

        if user_activity.score is None and user_activity.wish_movie is False:
            user_activity.delete()
        elif user_activity.score is not None:
            user_activity.comment = None
            user_activity.save()

        return Response({"info": "댓글이 삭제되었습니다."}, status=status.HTTP_202_ACCEPTED)


# wish adding
class MovieWish(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            movie = Movie.objects.get(pk=kwargs.get("pk"))
        except Movie.DoesNotExist:
            return Response({'error': '해당 영화가 존재하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        user = request.user
        try:
            active = UserActivity.objects.get(user=user,
                                              movie=movie)
        except UserActivity.DoesNotExist:
            return Response({'wish_movie': False}, status=status.HTTP_200_OK)
        return Response({'wish_movie': active.wish_movie}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        try:
            movie = Movie.objects.get(pk=kwargs.get("pk"))
        except Movie.DoesNotExist:
            return Response({'error': '해당 영화가 존재하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        user = request.user
        active = UserActivity.objects.get_or_create(user=user,
                                                    movie=movie)[0]
        if request.data.get("wish_movie") == "True":
            wish_movie = True
        elif request.data.get("wish_movie") == "False":
            wish_movie = False
        else:
            return Response({'error': '올바른 형식이 아닙니다.'}, status=status.HTTP_400_BAD_REQUEST)

        change_average = False

        if not active.wish_movie and active.watched_movie and wish_movie:
            count_all(movie, active.score, -1, user)
            active.score = float(0)
            change_average = True
            active.watched_movie = False

        active.wish_movie = wish_movie
        active.save()

        if change_average:
            average.score_average(movie)

        return Response({'wish_movie': active.wish_movie}, status=status.HTTP_200_OK)


# movie score
class MovieScore(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            movie = Movie.objects.get(pk=kwargs.get("pk"))
        except Movie.DoesNotExist:
            return Response({'error': '해당 영화가 존재하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        user = request.user
        try:
            active = UserActivity.objects.get(user=user,
                                              movie=movie)
        except UserActivity.DoesNotExist:
            return Response({'score': 0.0}, status=status.HTTP_200_OK)
        return Response({'score': active.score}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        try:
            movie = Movie.objects.get(pk=kwargs.get("pk"))
        except Movie.DoesNotExist:
            return Response({'error': '해당 영화가 존재하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        user = request.user
        active = UserActivity.objects.get_or_create(user=user,
                                                    movie=movie)[0]
        user_score = float(request.data.get("score"))
        if 0.5 <= user_score <= 5.0:
            active.score = user_score
            count_all(movie, active.score, +1, user)
            active.watched_movie = True
            active.wish_movie = False
            active.save()
            average.score_average(movie)
            return Response({'info': '점수가 올바르게 들어갔습니다.'}, status=status.HTTP_200_OK)
        elif user_score == 0.0:
            count_all(movie, active.score, -1, user)
            active.score = 0.0
            active.watched_movie = False
            active.save()
            average.score_average(movie)
            return Response({'info': '해당 영화의 평가가 리셋됩니다.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'score 값이 올바르지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)