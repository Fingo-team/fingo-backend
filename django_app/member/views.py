from django.db import IntegrityError
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
                return Response(ret, status=status.HTTP_200_OK)
        return Response({"error": "아이디 혹은 비밀번호가 올바르지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)


class UserLogout(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):

        if request.user.auth:
            request.user.auth_token.delete()
            return Response({"info": "정상적으로 로그인 되었습니다."}, status=status.HTTP_200_OK)
        return Response({"error": "이미 로그아웃 되었습니다."}, status=status.HTTP_400_BAD_REQUEST)


class UserSignUp(APIView):

    def post(self, request, *args, **kwargs):
        form = UserSignupForm(data=request.POST)
        if form.is_valid():
            try:
                FingoUser.objects.create_user(email=form.cleaned_data["email"],
                                              password=form.cleaned_data["password"],
                                              nickname=form.cleaned_data["nickname"])
            except IntegrityError as e:
                print(e.message)
                return Response({"error": "올바르지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
            fingo_user = authenticate(email=form.cleaned_data["email"],
                                      password=form.cleaned_data["password"])

            if fingo_user:
                token = Token.objects.get_or_create(user=fingo_user)[0]
                ret = {"token": token.key}
                return Response(ret, status=status.HTTP_200_OK)
        return Response({"error": "회원정보가 올바르지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)


