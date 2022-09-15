from __future__ import annotations
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from core.adapters import managers


class User(AbstractBaseUser, PermissionsMixin):
    """Model for storing user data"""

    registry = models.CharField(_("registration number"), max_length=256, unique=True)
    first_name = models.CharField(_("first name"), max_length=256)
    last_name = models.CharField(_("last name"), max_length=256)

    date_joined = models.DateField(_("date joined"), default=timezone.now)
    is_active = models.BooleanField(_("active"), default=True)
    is_staff = models.BooleanField(_("staff"), default=False)

    USERNAME_FIELD = "registry"

    objects = managers.UserManager()

    class Meta:
        """User model meta data"""

        verbose_name = _("user")
        verbose_name_plural = _("users")
