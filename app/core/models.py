from __future__ import annotations
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.conf import settings
from core import adapters


class User(AbstractBaseUser, PermissionsMixin):
    """Model for storing user data"""

    register = models.CharField(_("registration number"), max_length=256, unique=True)
    first_name = models.CharField(_("first name"), max_length=256)
    last_name = models.CharField(_("last name"), max_length=256)

    date_joined = models.DateField(_("date joined"), default=timezone.now)
    is_active = models.BooleanField(_("active"), default=True)
    is_staff = models.BooleanField(_("staff"), default=False)

    USERNAME_FIELD = "register"

    objects = adapters.UserManager()

    class Meta:
        """User model meta data"""

        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self) -> str:
        return f"{self.register} - {self.full_name}"

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


class ClassRoom(models.Model):
    """Model for storing class room data"""

    subject = models.CharField(_("subject"), max_length=256)
    name = models.CharField(_("name"), max_length=256)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name=_("members"),
    )
    school_days = models.IntegerField(default=100)
    start = models.DateField(_("start"))
    deadline = models.DateField(_("deadline"))

    class Meta:
        """Class room model meta data"""

        verbose_name = _("class room")
        verbose_name_plural = _("class rooms")


class Grade(models.Model):
    """Model for storing grades"""

    title = models.CharField(max_length=256)
    grade = models.IntegerField(_("grade"))
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("student"),
    )
    classroom = models.ForeignKey(
        ClassRoom,
        on_delete=models.CASCADE,
        verbose_name=_("class room"),
    )

    class Meta:
        """Grade model meta data"""

        verbose_name = _("grade")
        verbose_name_plural = _("grades")


class Absence(models.Model):
    """Model for storing absence objects"""

    absence_date = models.DateField(_("date"))
    classroom = models.ForeignKey(
        ClassRoom, on_delete=models.CASCADE, verbose_name=_("class room")
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_("student")
    )

    class Meta:
        """Absence model meta data"""

        verbose_name = _("absence")
        verbose_name_plural = _("absences")
