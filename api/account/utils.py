from django.core.mail import EmailMessage
from django.utils.translation import gettext as _


def send_code_email_confirm(email, code):
    message = EmailMessage(
        to=[email],
        subject=_('Код для подтверждения почты в приложении Terra Tort'),
        body=_(f'Здравствуйте!\n'
               f'Вы получили это письмо чтобы подтвердить электронную почту\n'
               f'Ваш код для подтверждения {code}.\nНикому не говорите ваш код\n'
               f'Если это были не вы, то ничего делать не нужно.'),
        from_email='terratort@gmail.com'
    )

    message.send()
    return True


