from __future__ import unicode_literals

# Create your models here.
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth import models as auth_models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('username'), unique=True, max_length=30)
    email = models.EmailField(_('email address'), blank=True, unique=False)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_staff = models.BooleanField(_('staff status'), default=True)
    is_superuser = models.BooleanField(_('superuser'), default=True)
    is_active = models.BooleanField(_('active'), default=True)

    MEMBER_CHOICES = [
        ('admin', 'admin'),
        ('mobile', 'mobile'),
        ('user', 'user'),
    ]
    member_type = models.CharField(
        max_length=10,
        choices=MEMBER_CHOICES,
        default='admin',
    )
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

