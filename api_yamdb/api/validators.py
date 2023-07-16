from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework.exceptions import ValidationError
from datetime import datetime


def validate_username(value):
    if value == 'me':
        raise ValidationError("Имя пользователя не может быть 'me'!")


class UsernameValidator(UnicodeUsernameValidator):
    regex = r'^[\w.@+-]+\Z'
    flags = 0
    message = (
        'Имя пользователя может содержать:'
        ' буквы, цифры '
        'и знаки @ . + -'
    )


def score_validator(score):
    if not 0 <= score <= 10:
        raise ValidationError('Оценка должна быть в диапазоне от 0 до 10!')


def validate_year(value):
    if value >= datetime.now().year:
        raise ValidationError(
            message=f'Год {value} больше текущего!',
            params={'value': value},
        )
