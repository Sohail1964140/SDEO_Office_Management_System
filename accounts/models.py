from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import myUserManager
# Create your models here.


class USER(AbstractUser):  
    
    username = None  
    email = models.EmailField(verbose_name="Email", unique=True, max_length = 40, null=False, blank=False)  
    image = models.ImageField(upload_to="user/profile/", null=True, blank=True)
    
    USERNAME_FIELD = 'email'  
    REQUIRED_FIELDS = []  
    
    objects = myUserManager()  