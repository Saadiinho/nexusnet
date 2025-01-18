<<<<<<< HEAD
from django.db import models
from authentification.models import User
# Create your models here.
class Publication(models.Model):
    message = models.TextField(max_length=1000)
    date = models.DateField()
    picture = models.ImageField(upload_to='', null=True, blank=True)
    isPrivate = models.BooleanField(default=False)
    like = models.PositiveIntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    def __str__(self):
        return f"{self.message} - {self.author}"
=======
from django.db import models
from authentification.models import User
# Create your models here.
class Publication(models.Model):
    message = models.TextField(max_length=1000)
    date = models.DateField()
    picture = models.ImageField(upload_to='', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    isPrivate = models.BooleanField(default=False)
    like = models.PositiveIntegerField(default=0)
    def __str__(self):
        return f"{self.message} - {self.author}"
>>>>>>> 710d29c1cf81e76015b4297a69c10f218c08b0b3
    