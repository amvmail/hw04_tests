from django.contrib.auth import get_user_model
from django.db import models


class ChangePassword(models.Model):
    old_password = models.CharField(max_length=20)
    new_password = models.CharField(max_length=20)
    confirm_new_password = models.CharField(max_length=20)


User = get_user_model()
