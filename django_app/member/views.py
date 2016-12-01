from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from django.contrib.auth import authenticate
from member.forms import FingoUserForm, UserSignupForm
from member.models import FingoUser


class UserLogin(APIView):

    def post(self, request, *args, **kwargs):
        form = FingoUserForm(data=request.POST)
        if form.is_valid():
            fingo_user = authenticate(email=form.cleaned_data["email"],
                                      password=form.cleaned_data["password"])

            if fingo_user:
                token = Token.objects.get_or_create(user=fingo_user)[0]
                ret = {"token": token.key}
                return Response(ret)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserLogout(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()

        return Response(status=status.HTTP_200_OK)


class UserSignUp(APIView):

    def post(self, request, *args, **kwargs):
        form = UserSignupForm(data=request.POST)
        if form.is_valid():
            try:
                FingoUser.objects.create_user(email=form.cleaned_data["email"],
                                              password=form.cleaned_data["password"],
                                              nickname=form.cleaned_data["nickname"])
            except:
                return Response({"error": "이미 존재하는 id 입니다."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                # send_mail
                pass
        #     fingo_user = authenticate(email=form.cleaned_data["email"],
        #                               password=form.cleaned_data["password"])
        #
        #     if fingo_user:
        #         token = Token.objects.get_or_create(user=fingo_user)[0]
        #         ret = {"token": token.key}
        #         return Response(ret)
        # return Response(status=status.HTTP_400_BAD_REQUEST)


class UserActivate(APIView):
    def get(self, request, *args, **kwargs):
        return Response(kwargs.get("useremail"))


