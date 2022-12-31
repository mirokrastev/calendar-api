from abc import ABC, abstractmethod
from random import randint

from django.apps import apps
from django.contrib.auth.tokens import default_token_generator

VerificationToken = apps.get_model('accounts', 'VerificationToken')


class BaseToken(ABC):
    TOKEN_TYPE = None

    @classmethod
    @abstractmethod
    def generate(cls, user):
        pass

    @classmethod
    def verify(cls, user, token):
        assert cls.TOKEN_TYPE is not None, 'TOKEN_TYPE attribute should be supplied'
        return VerificationToken.objects.filter(user=user, token=token, type=cls.TOKEN_TYPE).exists()


class AccountToken(BaseToken):
    TOKEN_TYPE = VerificationToken.Types.ACCOUNT

    @classmethod
    def generate(cls, user):
        # Generate 6 digit number
        return randint(100_000, 999_999)


class PasswordToken(BaseToken):
    TOKEN_TYPE = VerificationToken.Types.PASSWORD

    @classmethod
    def generate(cls, user):
        return default_token_generator(user)


token_service = {
    'account': AccountToken,
    'password': PasswordToken
}
