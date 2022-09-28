# Generated by Django 4.1.1 on 2022-09-27 22:45

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="teacherclassroom",
            name="user_id",
        ),
        migrations.AlterField(
            model_name="classroom",
            name="members",
            field=models.ManyToManyField(
                related_name="classrooms",
                to=settings.AUTH_USER_MODEL,
                verbose_name="members",
            ),
        ),
    ]
