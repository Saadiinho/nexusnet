<<<<<<< HEAD
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    profile_photo = models.ImageField(upload_to='' , default='default_profile_image.jpeg')

class Friend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_friends')

    def __str__(self):
=======
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    profile_photo = models.ImageField(upload_to='' , default='default_profile_image.jpeg')

class Friend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_friends')

    def __str__(self):
>>>>>>> 710d29c1cf81e76015b4297a69c10f218c08b0b3
        return f"{self.user.username} - {self.friend.username}"