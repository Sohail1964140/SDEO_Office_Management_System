from django.db import models
from Apps.schools.models import SCHOOL
from Apps.core.models import POST, GENDER_CHOICES, YesNo
from django.utils.timezone import now
from .managers import PimaryTeachers,TotalTeachers
# Create your models here.

class TEACHER(models.Model):
    
    school = models.ForeignKey(SCHOOL, on_delete=models.CASCADE, related_name="teachers")
    post = models.ForeignKey(POST, on_delete=models.CASCADE, related_name="teachers")
    name = models.CharField(max_length=30)
    fname = models.CharField(max_length=30, verbose_name="Father Name")
    g_fund_no = models.CharField(max_length=15, verbose_name="GP Fund Number")
    salary = models.CharField(max_length=15)
    cnic = models.CharField(max_length=17)
    image = models.ImageField(upload_to="images/teacher/profile", blank=True, null=True,verbose_name="Profile Image",)
    address = models.TextField(max_length=200)
    dob = models.DateField(verbose_name="DOB")
    personal_no = models.CharField(max_length=10, unique=True, verbose_name="Personal Number")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    isInPrimarySchool = models.BooleanField(default=True,choices=YesNo, null=True, blank=True)
    dateOfTakingOverChargeInPresentSchool = models.DateField(verbose_name="Date of taking over charge in present school", default=now)
    dateOfTakingOverChargeOnPresentPost = models.DateField(verbose_name="Date of taking over charge on present post", default=now)
    objects = PimaryTeachers()
    totalTeachers = TotalTeachers()
    
    @property
    def get_teacher(self):
        
        return f'{self.name} - {self.personal_no}'
    @property
    def get_contact(self):
        return self.contacts.all().first()
    
    def __str__(self):
        
        return self.get_teacher
    
    class Meta:
        ordering = ['pk']


class CONTACT(models.Model):
    
    teacher = models.ForeignKey(TEACHER, on_delete=models.CASCADE, related_name="contacts")
    contact = models.CharField(max_length=11, unique=True)
    
    


class TeacherProffQualification(models.Model):
    
    teacher = models.ForeignKey(TEACHER, on_delete=models.CASCADE, related_name="Proffqualification")
    name = models.CharField(max_length=15, verbose_name="New Professional Qualification")
    
    
    class Meta:
        unique_together  = ['teacher', 'name']
        verbose_name = "Teacher Professional Qualification"

class TeacherAccadQualification(models.Model):
    
    teacher = models.ForeignKey(TEACHER, on_delete=models.CASCADE, related_name="Accadqualification")
    name = models.CharField(max_length=15, verbose_name="New Academic Qualification")
    
    
    class Meta:
        unique_together  = ['teacher', 'name']
        verbose_name = 'Teacher Accadmic Qualification'

class TeacherFirstAppointment(models.Model):
    
    teacher = models.OneToOneField(TEACHER,on_delete=models.CASCADE, related_name="teacherFirstAppointment")
    appointmentPost = models.ForeignKey(POST, on_delete=models.CASCADE,verbose_name="Post", related_name="teacherAppointments")
    dateOfFirstAppointment = models.DateField(verbose_name="Date of first appointment")




class Transfer(models.Model):
    
    teacher = models.ForeignKey(TEACHER, on_delete=models.CASCADE, related_name="transfers", verbose_name="Teacher")
    fromSchool = models.ForeignKey(SCHOOL, on_delete=models.CASCADE, related_name='fromTransfers', verbose_name="From School")
    toSchool = models.ForeignKey(SCHOOL, on_delete=models.CASCADE, related_name="toTransfers", verbose_name="To School", null=True, blank=True, default=None)
    date = models.DateField(default=now)


class Promotion(models.Model):
    
    teacher = models.ForeignKey(TEACHER, on_delete=models.CASCADE, related_name="promotions", verbose_name="Teacher")
    fromPost = models.ForeignKey(POST, on_delete=models.CASCADE, related_name='fromPromotions', verbose_name="From Post")
    toPost = models.ForeignKey(POST, on_delete=models.CASCADE, related_name="toPromotionss", verbose_name="Post", null=True, blank=True)
    date = models.DateField(default=now)


    
class TeacherMonthlyEntry(models.Model):
    
    teacher = models.ForeignKey(TEACHER, on_delete=models.CASCADE, related_name="TMEs")
    school = models.ForeignKey(SCHOOL, on_delete=models.CASCADE, related_name="TME")
    post = models.ForeignKey(POST, on_delete=models.CASCADE, related_name="TMEs")
    salary = models.PositiveIntegerField()
    date = models.DateField(default=now)
    
    class Meta:
        unique_together = ['teacher', 'school', 'date']