from django.db import models
from django.urls import reverse
from autoslug import AutoSlugField
from django.utils.text import slugify
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy as _
"""
=== ============ === Some Common CHOICES === ============ === 
"""
STATUS_CHOICE = (('1', 'Active'), ('0', 'In-Active'))
PBS_CHOICE = (('3','3'),('4', '4'), ('12', '12'),('13', '13'), ('14', '14'),('15', '15'))
YesNo  = [(True, 'Yes'), (False, 'No')]
GENDER_CHOICES = (('1', 'Male'),('0', 'FeMale'))
CLASS_CHOICES = [
    ('1', 'Kachi'),
    ('2', 'Pki'),
    ('3', '2nd'),
    ('4', '3rd'),
    ('5', '4th'),
    ('6', '5th'),
]

def hx_Redirect(url):
    resp = HttpResponseRedirect(_(url))
    resp['HX-Redirect'] = _(url)
    return resp

class CIRCLE(models.Model):
    name = models.CharField(max_length=60, unique=True, blank=False, null=False)
    slug = AutoSlugField(populate_from="name", unique=True)
    
    def __str__(self):
        return self.name

    def get_update_url(self):
        return reverse("core:circleUpdate", kwargs={"name": self.slug})
    
    def get_delete_url(self):
        return reverse("core:circleDelete", kwargs={"name": self.slug})
    
    class Meta:
        ordering = ['-pk']
    


class UC(models.Model):
    
    circle = models.ForeignKey(to="CIRCLE", on_delete=models.CASCADE, related_name="UCs")
    name = models.CharField(max_length=255, unique=True, blank=False, null=False)
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Union_Council'
        verbose_name = 'Union Council'
        verbose_name_plural = 'Union Councils'
        ordering = ['pk']

class VC(models.Model):
    
    uc = models.ForeignKey(to="UC", on_delete=models.CASCADE, verbose_name="Union Council", related_name="VCs")
    name = models.CharField(max_length=255, unique=True, blank=False, null=False)
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Village_Council'
        verbose_name = 'Village Council'
        verbose_name_plural = 'Village Councils'



class CLASS(models.Model):
    
    name = models.CharField(max_length=60, unique=True, null=False, verbose_name="Class Name")
    status = models.CharField(max_length=1, choices=STATUS_CHOICE, default=1)
    
    def __str__(self):
        return self.name
    

class POST(models.Model):
    name = models.CharField(max_length=20)
    bps = models.CharField(max_length=2, choices=PBS_CHOICE, verbose_name="Scale")
    
    def __str__(self):
        return f'{self.name} - {self.bps}'
    
    class Meta:
        
        unique_together = ['name', 'bps']
        ordering = ['bps']



class ITEM_CATEGORY(models.Model):
    name = models.CharField(max_length=40, unique=True, null=True, verbose_name="Item Category")

    def __str__(self):
        return self.name


class STOCK_ITEM(models.Model):
    name = models.CharField(max_length=255, unique=True, null=True, verbose_name="Stock Item")
    category = models.ForeignKey('ITEM_CATEGORY', on_delete=models.CASCADE, related_name="items")
    
    def __str__(self):
        return self.name
    
class BANK(models.Model):
    
    name = models.CharField(max_length=30, unique=True, null=False)
    slug = AutoSlugField(populate_from="name", unique=True, default="-")
    def __str__(self):
        return self.name

    def get_update_url(self):
        return reverse("core:bankUpdate", kwargs={"name": self.slug})
    
    def get_delete_url(self):
        return reverse("core:bankDelete", kwargs={"name": self.slug})
    
    class Meta:
        ordering = ['-pk']
    
class CHAIRMAN(models.Model):
    
    name = models.CharField(max_length=30, unique=True, null=False)
    contact = models.CharField(max_length=11, unique=True, null=False)
    slug = AutoSlugField(populate_from="name", unique=True, default="-")
    def __str__(self):
        return f"{self.name} - {self.contact}"

    def get_update_url(self):
        return reverse("core:chairmanUpdate", kwargs={"name": self.slug})
    
    def get_delete_url(self):
        return reverse("core:chairmanDelete", kwargs={"name": self.slug})
    
    class Meta:
        ordering = ['-pk']