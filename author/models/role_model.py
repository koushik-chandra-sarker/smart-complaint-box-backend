from django.db import models


class Role(models.Model):
    ADMIN = 1
    MODERATOR = 2
    GENERAL = 3
    ROLE_CHOICES = (
        (ADMIN, 'admin'),
        (MODERATOR, 'moderator'),
        (GENERAL, 'general'),
    )

    id = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=GENERAL, primary_key=True)

    def __str__(self):
        return self.get_id_display()
