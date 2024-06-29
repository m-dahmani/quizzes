# Generated by Django 4.2.13 on 2024-06-29 04:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("quizzes", "0003_auto_20240628_2250"),
    ]

    operations = [
        migrations.CreateModel(
            name="Course",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name="CourseQuiz",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("information", models.CharField(blank=True, max_length=255)),
                ("position", models.IntegerField()),
                ("optional", models.BooleanField(default=False)),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="quizzes.course"
                    ),
                ),
                (
                    "quiz",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="quizzes.quiz"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="course",
            name="quizzes",
            field=models.ManyToManyField(
                related_name="informations",
                through="quizzes.CourseQuiz",
                to="quizzes.quiz",
            ),
        ),
    ]