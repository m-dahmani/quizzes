from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class User(AbstractUser):

    # QUIZMASTER = 'QUIZMASTER'

    ROLE_CHOICES = (
        ('QUIZMASTER', 'Quizmaster'),

    )
    # extend AbstractUser and add two more fields
    role = models.CharField(choices=ROLE_CHOICES, max_length=30, verbose_name='Role', null=True)

    def save(self, *args, **kwargs):
        """
        Update User's save() method to ensure that any new users added after migration are
        automatically assigned to the correct group based on their role Without this update to the save() method,
        only existing users at the time of migration will be correctly assigned to groups,
        and new users will have to be assigned manually.
        Automatic assignment of new users: Each time a new user is created and saved,
        they will automatically be added to the group corresponding to their role.
        Changing the role of existing users:
        If the role of an existing user is changed, the user will be added to the corresponding new group.
        """
        super().save(*args, **kwargs)
        # to override the save method in order to add new users assigned to groups automatically after migration
        if self.role == 'QUIZMASTER':
            group = Group.objects.get(name='quizmasters')
            if not group.user_set.filter(id=self.id).exists():
                # assign existing users in the database with the Group.user_set.add() function
                group.user_set.add(self)





