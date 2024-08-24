from django.core.mail import EmailMessage


def send_email_code(email, code):
    message = EmailMessage(
        to=[email],
        subject='Код для регистрации в приложении Terra Tort',
        body=f'Здравствуйте!\n'
               f'Вы получили это письмо для регистрации\n'
               f'Ваш код для регистрации {code}.\nНикому не говорите ваш код\n'
               f'Если это были не вы, то ничего делать не нужно.',
        from_email='terratort@gmail.com'
    )
    message.send()
    return True


def send_email_code_for_reset(email, code):
    message = EmailMessage(
        to=[email],
        subject='Код для сброса пароля в приложении Terra Tort',
        body=f'Здравствуйте!\n'
               f'Вы получили это письмо чтобы сбросить пароль\n'
               f'Ваш код для сброса {code}.\nНикому не говорите ваш код\n'
               f'Если это были не вы, то ничего делать не нужно.',
        from_email='terratort@gmail.com'
    )
    message.send()
    return True
