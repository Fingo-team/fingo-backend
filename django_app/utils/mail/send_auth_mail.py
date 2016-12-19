from django.conf import settings
from django.core.mail import send_mail


__all__ = [
    'send_activation_mail',
]


def send_activation_mail(user_email, hashed_email):
    hashed_email = hashed_email.replace("$pbkdf2-sha512$8000$", "")
    activate_url = "http://eb-fingo-real.ap-northeast-2.elasticbeanstalk.com/api/v1.0/user/activate/{hashed_email}/".format(hashed_email=hashed_email)
    send_mail(
        "Fingo Service activation mail",
        """
        저희 Fingo 서비스를 이용해 주셔서 감사합니다.
        아래 url을 누르면 계정이 활성화 됩니다.
        {activate_url}
        """.format(activate_url=activate_url),
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
    )
