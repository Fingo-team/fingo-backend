class UserActionOrdering:

    def get_ordering_param(self, ordering_request):
        if ordering_request == "activity_time" or ordering_request is None:
            ordering = "-activity_time"
        elif ordering_request == "title":
            ordering = "movie__title"
        elif ordering_request == "score":
            ordering = "-movie__score"

        return ordering