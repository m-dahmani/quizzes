from django.contrib.auth.models import Group, Permission
from django.conf import settings
from django.db import models


class Quiz(models.Model):

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100)
    # Adds an author field as a foreign key to the user.
    # Use settings.AUTH_USER_MODEL to reference the custom user model if necessary.
    # Each quiz can only have one author
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quizzes')
    # related_name='quizzes' : allows access to a user's quizzes via user.quizzes.all().

    #  Add custom permission (deactivate_quiz) to the Quiz Model
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    # In the Quiz model, the deactivate_quiz permission is added to allow moderators to disable quizzes.
    class Meta:
        # Specify custom permissions by configuring the permissions attribute in a Meta class of a model
        permissions = [
            ("deactivate_quiz", "Can deactivate quiz")
        ]

    def send_email_to_author(self):
        # Implement email sending logic here
        pass

    def save(self, *args, **kwargs):
        # Calling the parent's save() method to save the object
        super().save(*args, **kwargs)
        # Add & call easily the send_email_to_author() method to send an email to the author
        self.send_email_to_author()

        # Ajouter l'utilisateur au groupe "moderators" et lui attribuer la permission "deactivate_quiz"
        try:
            deactivate_quiz = Permission.objects.get(codename='deactivate_quiz')
            moderators, created = Group.objects.get_or_create(name='moderators')

            # Assigner la permission au groupe s'il ne l'a pas déjà
            if not moderators.permissions.filter(id=deactivate_quiz.id).exists():
                moderators.permissions.add(deactivate_quiz)

            # Ajouter l'utilisateur au groupe s'il ne fait pas déjà partie
            if not moderators.user_set.filter(id=self.id).exists():
                moderators.user_set.add(self)
        except Permission.DoesNotExist:
            print("Permission 'deactivate_quiz' does not exist.")
        except Group.DoesNotExist:
            print("Group 'moderators' does not exist.")


class Course(models.Model):

    # Add & Update a M2M to Quiz and tell it to use the intermediate table via through
    # access all Quiz instances having the User as a contributor using user.informations instead

    name = models.CharField(max_length=200)
    # Define a ManyToManyField in Course that links it to Quiz, named quizzes
    # Specify the CourseQuiz Model with the through argument when specifying this field
    quizzes = models.ManyToManyField(Quiz, through='CourseQuiz', related_name='informations')


class CourseQuiz(models.Model):
    """
        The intermediate table requires two ForeignKey to the two models involved in the ManyToMany relationship
        Specify the CourseQuiz Model with the through argument when specifying this field
        CourseQuiz: This intermediate model stores additional information (position and optional) for each relationship
         between a Course and a Quiz.
        Course: The ManyToManyField uses through='CourseQuiz' to specify that the relationship is managed
        by the CourseQuiz model.
    """

    # a relationship to the Course
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    # a relationship to the Quiz
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    # to store information about information specific to each author
    information = models.CharField(max_length=255, blank=True)
    position = models.IntegerField()
    optional = models.BooleanField(default=False)




