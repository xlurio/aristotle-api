from django.contrib.auth.models import BaseUserManager, Group
from django.contrib.auth.hashers import make_password


class UserManager(BaseUserManager):
    def _create_user(self, password, **kwargs):
        registry = kwargs.get("registry")

        if not registry:
            raise ValueError("A registration number must be set")

        new_user = self.model(**kwargs)
        new_user.password = make_password(password)
        new_user.save(using=self._db)

        return new_user

    def create_user(self, password, **kwargs):
        kwargs.setdefault("is_staff", False)
        kwargs.setdefault("is_superuser", False)

        return self._create_user(password, **kwargs)

    def create_professor(self, password, **kwargs):
        professor_group, created = Group.objects.get_or_create(name="professor")

        professor = self.create_user(password, **kwargs)
        professor.groups.add(professor_group)

        professor.save(using=self._db)

        return professor

    def create_student(self, password, **kwargs):
        student_group, created = Group.objects.get_or_create(name="student")

        student = self.create_user(password, **kwargs)
        student.groups.add(student_group)

        student.save(using=self._db)

        return student

    def create_superuser(self, password, **kwargs):
        kwargs["is_staff"] = True
        kwargs["is_superuser"] = True

        return self._create_user(password=password, **kwargs)
