from rest_framework.exceptions import APIException
from rest_framework import status


class OrderingSelectException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = u"올바르지 않은 카테고리 선택."


class OrderingSelect:

    def get_ordering_param(self, ordering_request):
        try:
            if ordering_request == "activity_time" or ordering_request is None:
                ordering = "-activity_time"
            elif ordering_request == "title":
                ordering = "movie__title"
            elif ordering_request == "score":
                ordering = "-movie__score"

            return ordering
        except:
            raise OrderingSelectException()
