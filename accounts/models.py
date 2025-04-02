from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O email é obrigatório.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superusuários precisam ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superusuários precisam ter is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(_('Email'), unique=True)
    first_name = models.CharField(_('Primeiro nome'), max_length=150, blank=True, db_index=True)
    last_name = models.CharField(_('Sobrenome'), max_length=150, blank=True, db_index=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta():
        db_table = "accounts"
        verbose_name = _("Usuário")
        verbose_name_plural = _("Usuários")

    def __str__(self):
        return self.email

    objects = CustomUserManager()
