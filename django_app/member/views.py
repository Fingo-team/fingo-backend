import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from django.contrib.auth import authenticate
from member.forms import FingoUserForm, UserSignupForm
from member.models import FingoUser, UserHash


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
                if "email" in str(e):
                    return Response({"error": "이미 존재하는 email 입니다."}, status=status.HTTP_400_BAD_REQUEST)
                elif "nickname" in str(e):
                    return Response({"error": "이미 존재하는 nickname 입니다."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"info": "인증메일이 발송 되었습니다."}, status=status.HTTP_200_OK)


class UserActivate(APIView):
    def get(self, request, *args, **kwargs):

        hashed_email = "$pbkdf2-sha512$8000$"+kwargs.get("hash")+settings.SECRET_KEY
        try:
            active_ready_user = UserHash.objects.get(hashed_email=hashed_email)
        except ObjectDoesNotExist:
            return Response({"error": "인증요청 url이 잘못되었습니다."}, status=status.HTTP_400_BAD_REQUEST)
        active_ready_user.user.is_active = True
        active_ready_user.user.save()
        return Response({"info": "계정이 활성화 되었습니다."}, status=status.HTTP_200_OK)


class UserFacebookLogin(APIView):

    def post(self, request, *args, **kwargs):
        ACCESS_TOKEN = kwargs.get("access_token")
        url_debug_token = 'https://graph.facebook.com/debug_token?' \
                          'input_token={it}&' \
                          'access_token={at}'.format(
                          it=ACCESS_TOKEN,
                          at=settings.FB_APP_ACCESS_TOKEN
        )
        r = requests.get(url_debug_token)
        debug_token = r.json()
        # USER_ID = debug_token['data']['user_id']
        return Response(debug_token)
