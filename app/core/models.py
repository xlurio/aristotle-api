from __future__ import annotations

from datetime import date

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core import adapters


class User(AbstractBaseUser, PermissionsMixin):
    """Model for storing user data"""

    register = models.CharField(_("registration number"), max_length=255, unique=True)
    first_name = models.CharField(_("first name"), max_length=255)
    last_name = models.CharField(_("last name"), max_length=255)

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

    subject = models.CharField(_("subject"), max_length=255)
    name = models.CharField(_("name"), max_length=255)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, verbose_name=_("members"), related_name="classrooms"
    )
    school_days = models.IntegerField(default=100)
    start = models.DateField(_("start"))
    deadline = models.DateField(_("deadline"))

    class Meta:
        """Class room model meta data"""

        verbose_name = _("class room")
        verbose_name_plural = _("class rooms")

    @property
    def is_active(self) -> bool:
        """Property to inform if the classroom is active"""
        today = date.today()
        did_class_begun = today > self.start
        did_class_ended = today > self.deadline
        return did_class_begun and not did_class_ended


class Grade(models.Model):
    """Model for storing grades"""

    title = models.CharField(max_length=255)
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


# Read only


class StudentClassroom(models.Model):
    """Model for reading student class room data"""

    user_id = models.IntegerField(null=False)
    classroom_id = models.IntegerField(null=False)
    student = models.CharField(_("student"), max_length=255)


class TeacherClassroom(models.Model):
    """Model for reading teacher class room data"""

    classroom_id = models.IntegerField(null=False)
    classroom = models.CharField(_("class room"), max_length=255)


class ClassroomStudent(models.Model):
    """Model for reading class room student data"""

    student = models.CharField(_("student"), max_length=255)
    classroom = models.ForeignKey(
        TeacherClassroom, on_delete=models.CASCADE, related_name="students"
    )


class ClassroomGrade(models.Model):
    """Model for reading grade data"""

    average = models.FloatField(_("average"), max_length=255, default=0.0)
    classroom = models.ForeignKey(
        StudentClassroom,
        on_delete=models.CASCADE,
        related_name="grades",
    )
    student = models.ForeignKey(
        ClassroomStudent, on_delete=models.CASCADE, related_name="grades"
    )


class GradeDetail(models.Model):
    """Model for reading grade details"""

    title = models.CharField(_("title"), max_length=255)
    grade_value = models.IntegerField(_("grade value"))
    classroom_grade = models.ForeignKey(
        ClassroomGrade,
        on_delete=models.CASCADE,
        related_name="grade_values",
    )


class ClassroomAbsence(models.Model):
    """Model for reading absence data"""

    absence_amount = models.IntegerField(_("absence amount"), default=0)
    frequency = models.FloatField(_("frequency"), default=1.0)
    classroom = models.ForeignKey(
        StudentClassroom,
        on_delete=models.CASCADE,
        related_name="absences",
    )
    student = models.ForeignKey(
        ClassroomStudent, on_delete=models.CASCADE, related_name="absences"
    )


class AbsenceDetail(models.Model):
    """Model for reading absence dates data"""

    absence_date = models.DateField(_("date"))
    classroom_absence = models.ForeignKey(
        ClassroomAbsence,
        on_delete=models.CASCADE,
        related_name="absence_dates",
    )
