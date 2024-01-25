from django.db import models

class PimaryTeachers(models.Manager):
    
    def get_queryset(self) :
        return super().get_queryset().filter(isInPrimarySchool=True)


class TotalTeachers(models.Manager):
    
    def get_queryset(self):
        return super().get_queryset()
    