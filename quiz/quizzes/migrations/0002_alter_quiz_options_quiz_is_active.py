# Generated by Django 4.2.13 on 2024-06-28 22:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("quizzes", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="quiz",
            options={"permissions": [("deactivate_quiz", "Can deactivate quiz")]},
        ),
        migrations.AddField(
            model_name="quiz",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
    ]
