import requests
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datastructures import MultiValueDictKeyError
from django.conf import settings
from django.contrib.auth import authenticate
from django.core.files.base import ContentFile

from member.serializations import UserCreateSerializer, UserLoginSerializer
from member.models import FingoUser, UserHash
from apis.image_file.resizing_image import create_thumbnail


class UserLogin(APIView):

    def post(self, request, *args, **kwargs):
        serial_data = UserLoginSerializer(request.data)
        fingo_user = authenticate(email=serial_data.data["email"],
                                  password=serial_data.data["password"])

        if fingo_user:
            token = Token.objects.get_or_create(user=fingo_user)[0]
            ret = {"token": token.key}
            return Response(ret, status=status.HTTP_200_OK)
        return Response({"error": "아이디 혹은 비밀번호가 올바르지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)


class UserLogout(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):

        if request.user:
            request.user.auth_token.delete()
            return Response({"info": "정상적으로 로그아웃 되었습니다."}, status=status.HTTP_200_OK)
        return Response({"error": "이미 로그아웃 되었습니다."}, status=status.HTTP_400_BAD_REQUEST)


class UserSignUp(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserCreateSerializer

    def create(self, request, *args, **kwargs):
        serial_data = self.get_serializer(data=request.data)
        if serial_data.is_valid():
            try:
                serial_data.save()
            except IntegrityError as e:
                if "email" in str(e):
                    return Response({"error": "이미 존재하는 email 입니다."}, status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response({"info": "인증메일이 발송 되었습니다."}, status=status.HTTP_200_OK)

        else:
            return Response({'info': '입력형식이 올바르지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)


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


class UserProfileImgUpload(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.auth.user
        try:
            user_img = request.FILES["user_img"]
        except MultiValueDictKeyError:
            return Response({"error": "이미지를 선택하지 않았습니다."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            temp_img, img_name = create_thumbnail(user_img)
            content_file = ContentFile(temp_img.read())
            user.user_img.save(img_name+".jpg", content_file)
            temp_img.close()
            content_file.close()
        return Response({"info": "프로필 이미지를 등록하였습니다."}, status=status.HTTP_201_CREATED)


class UserFacebookLogin(APIView):

    def post(self, request, *args, **kwargs):
        access_token = request.data.get("access_token")
        url_debug_token = 'https://graph.facebook.com/debug_token?' \
                          'input_token={it}&' \
                          'access_token={at}'.format(
                            it=access_token,
                            at=settings.FB_APP_ACCESS_TOKEN
                          )
        r = requests.get(url_debug_token)
        debug_token = r.json()
        if debug_token['data']['is_valid']:
            user_id = debug_token['data']['user_id']
            try:
                facebook_user = FingoUser.objects.get(facebook_id=user_id)
            except FingoUser.DoesNotExist:
                user_info = self.get_user_info(user_id, access_token)
                facebook_user = FingoUser.objects.create_facebook_user(facebook_id=user_id,
                                                                       nickname=user_info['name'])
            token = Token.objects.get_or_create(user=facebook_user)[0]
            ret = {"token": token.key}
            return Response(ret, status=status.HTTP_200_OK)
        else:
            return Response({'error': debug_token['data']['error']['message']})

    def get_user_info(self, user_id, access_token):
        url_request_user_info = 'https://graph.facebook.com/' \
                                '{user_id}?' \
                                'fields=id,name&' \
                                'access_token={access_token}'.format(
            user_id=user_id,
            access_token=access_token
        )
        r = requests.get(url_request_user_info)
        user_info = r.json()
        return user_info


class TestView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        return Response({"msg": "test complete"})
