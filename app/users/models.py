from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    class RoleChoices(models.TextChoices):
        USER = 'user', _('User')
        MODERATOR = 'moderator', _('Moderator')
        ADMIN = 'admin', _('Admin')

    email = models.EmailField('email address', blank=False, unique=True)
    bio = models.TextField(max_length=500, blank=True, verbose_name='Информация о себе')
    role = models.CharField(max_length=50, choices=RoleChoices.choices, default=RoleChoices.USER)
    confirmation_code = models.CharField(max_length=100, blank=True, )

    def __str__(self):
        return self.email

    def get_tokens(self):
        tokens = RefreshToken.for_user(self)
        return {
            'refresh': str(tokens),
            'access': str(tokens.access_token)}
