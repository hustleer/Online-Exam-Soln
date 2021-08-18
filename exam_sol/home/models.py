from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.db import models
from django.contrib.auth.models import PermissionsMixin , AbstractBaseUser , BaseUserManager
from django.db.models.base import Model
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
# from user.models import LikeStore
# from product.models import Product
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe

# Create your models here.
from django.forms import ModelForm, TextInput, Textarea
from django.http import request
from django.utils.safestring import mark_safe


class UserManager(BaseUserManager):
    def create_user(self , name , password = None):
        user = self.model( name= name )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser( self , name , password ):
        user = self.create_user( name = name , password = password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class CustomUser(PermissionsMixin , AbstractBaseUser):
    STATUS = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )
    name = models.CharField(max_length=30 , unique=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()
    create_at=models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'name'

    def __str__(self):
        return self.name

class QuestionAnwers(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    # pidit = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    pidit=models.CharField(max_length=1000 , null=True)
    answer=models.CharField(max_length=1000)
    question=models.CharField(max_length=1000)
    status=models.CharField(max_length=10, choices=STATUS , default='True')
    
    def __str__(self):
        return self.question
    
 