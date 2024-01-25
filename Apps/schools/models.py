from django.db import models
from Apps.core.models import UC
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from django.utils.text import slugify
# Create your models here.

USER = get_user_model()


class SCHOOL(models.Model):
    
    emis = models.PositiveIntegerField(verbose_name="EMIS",unique=True, blank=False, null=False,validators=[MaxValueValidator(9999999)])
    name = models.CharField(max_length=255, unique=True, blank=False, null=False)
    uc = models.ForeignKey(to=UC, on_delete=models.CASCADE, related_name="schools", verbose_name="Union Council") 
    user = models.OneToOneField(to=USER, on_delete=models.CASCADE)    
    latitude = models.FloatField()
    langitude = models.FloatField()
    ddo = models.CharField(verbose_name="DDO Code", unique=True, blank=False, null=False, max_length=15)
    yearOfConstruction = models.DateTimeField(verbose_name="Year of Construction")
    slug = models.SlugField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug =  slugify(self.name)
        super().save(*args, **kwargs)
    
    
    class Meta:
        ordering = ['pk']
