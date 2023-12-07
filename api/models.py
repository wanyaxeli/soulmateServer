from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from cloudinary.models import CloudinaryField
# Create your models here.
user=settings.AUTH_USER_MODEL
class User(AbstractUser):
    email = models.EmailField(default='email address', unique=True)
    confirm_password=models.CharField(max_length=255)
    gender=models.CharField(max_length=255)
    username=None
    
    USERNAME_FIELD='email'
    REQUIRED_FIELDS = ['username']
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
class ProfileImages(models.Model):
    user=models.ForeignKey(user,on_delete=models.CASCADE)
    image=CloudinaryField('image')
    def __str__(self) -> str:
        return self.user.first_name
class Profile(models.Model):
    user=models.OneToOneField(user,on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
class Interests(models.Model):
    user=models.ForeignKey(user,on_delete=models.CASCADE)
    interest=models.JSONField()
    def __str__(self):
        return self.user.first_name
class Messages(models.Model):
    sender=models.ForeignKey(user,on_delete=models.CASCADE,related_name='sender')
    receipient=models.ForeignKey(user,on_delete=models.CASCADE,related_name='receipient')
    message=models.CharField(max_length=2000,default='',null=True)
    read=models.BooleanField(default=False)
    def __str__(self) -> str:
        return self.pk
class Likes(models.Model):
    user=models.ForeignKey(user,on_delete=models.CASCADE,related_name='owner')
    myLikes=models.ManyToManyField(User)
   
    def __str__(self):
        return self.user.first_name 


