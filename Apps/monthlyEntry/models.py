from django.db import models
from Apps.schools.models import SCHOOL
from django.utils.timezone import now
from Apps.core.models import CLASS_CHOICES, POST, STOCK_ITEM, YesNo, CHAIRMAN, BANK
from Apps.staff.models import TEACHER,TeacherProffQualification, TeacherAccadQualification
from django.db.models import Sum
# Create your models here.


class MonthlyRecord(models.Model):
    
    date = models.DateField(default=now)
    school = models.ForeignKey(to=SCHOOL, on_delete=models.CASCADE, related_name="records")

    def __str__(self):
        
        return f'{self.school} - {self.date}'


class SchoolBuilding(models.Model):
    
    
    record = models.ForeignKey(to=MonthlyRecord, on_delete=models.CASCADE, related_name="building")
    yearOfConstruction = models.DateField(verbose_name="Year of Construction")
    waterSource = models.BooleanField(choices=YesNo, default=True, verbose_name="Water Source")
    boundryWall = models.BooleanField(choices=YesNo, default=True, verbose_name="Boundry Wall")
    playGroud  = models.BooleanField(choices=YesNo, default=False, verbose_name="Play Ground")   
    noOfToilets = models.CharField(max_length=2,verbose_name="No of Toilets") 
    scienceLaboratory = models.BooleanField(choices=YesNo, verbose_name="Science Laboratory")
    computerLaboratory = models.BooleanField(choices=YesNo, verbose_name="Computer Laboratory")
    coverdArea = models.CharField(max_length=10, verbose_name="Coverd")
    uncoverdArea = models.CharField(max_length=10, verbose_name="UnCoverd")
    noOfClassRooms = models.CharField(max_length=2, verbose_name="No of Class Rooms")
    noOfOtherRooms = models.CharField(max_length=2, verbose_name="No of Other Rooms")
    fruitTrees = models.CharField(max_length=2, verbose_name="Fruit Trees")
    shadyTrees = models.CharField(max_length=2, verbose_name="Shady Trees")
    internalElectrification = models.BooleanField(choices=YesNo,verbose_name="Internal Electrification")
    electricSuply = models.BooleanField(choices=YesNo, verbose_name="Electric Suply")





class StudentStrength(models.Model):
    
    record = models.ForeignKey(to=MonthlyRecord, on_delete=models.CASCADE, related_name="studentStrength")
    classID = models.CharField(max_length=1, choices=CLASS_CHOICES)
    boys = models.CharField(max_length=3)
    girls = models.CharField(max_length=3)
    
    @property
    def total_girls(self):        
        return  self.record.studentStrength.all().aggregate(no_of_girls = Sum('girls'))['no_of_girls']
    
    @property
    def total_boys(self):        
        return  self.record.studentStrength.all().aggregate(no_of_boys = Sum('boys'))['no_of_boys']
    
    @property
    def total(self):
        
        return self.total_boys + self.total_girls
    
    @property
    def total_in_class(self):
        return int(self.boys) + int(self.girls)
    
    
    
class TeacherMonthlyEntry(models.Model):
    
    record = models.ForeignKey(to=MonthlyRecord, on_delete=models.CASCADE ,related_name="teachersRecords")
    teacher = models.ForeignKey(to=TEACHER, on_delete=models.CASCADE, related_name="teacherRecords")
    post = models.ForeignKey(to=POST, on_delete=models.SET_NULL, null=True)
    salary = models.CharField(max_length=10)
    dateOfTakingOverChargeOnPresentPost = models.DateField(verbose_name="date Of Taking Over Charge On Present Post", default=now)
    dateOfTakingOverChargeInPresentSchool = models.DateField(verbose_name="date Of Taking Over Charge In Present School", default=now)
    
    
    
class MonthlyRecordForProfessionalQualification(models.Model):
    
    teacherEntry = models.ForeignKey(to=TeacherMonthlyEntry, related_name="proffessionalQualification",on_delete=models.CASCADE)
    qualification = models.ForeignKey(to=TeacherProffQualification,  on_delete=models.CASCADE)

class MonthlyRecordForAcademicQualification(models.Model):
    
    teacherEntry = models.ForeignKey(to=TeacherMonthlyEntry, related_name="AccademicQualification",on_delete=models.CASCADE)
    qualification = models.ForeignKey(to=TeacherAccadQualification,  on_delete=models.CASCADE)



class SchoolStock(models.Model):
    
    record = models.ForeignKey(to=MonthlyRecord, on_delete=models.CASCADE, related_name="stock")
    item = models.ForeignKey(to=STOCK_ITEM, on_delete=models.CASCADE)
    noOfItems = models.CharField(max_length=5, verbose_name="No of Items")
    required = models.CharField(max_length=5)
    surplus = models.CharField(max_length=5)


class StaffAvalibility(models.Model):
    
    record = models.ForeignKey(to=MonthlyRecord, on_delete=models.CASCADE, related_name="staffs")
    post = models.ForeignKey(to=POST, on_delete=models.CASCADE)
    sanctioned = models.CharField(max_length=1)
    filled = models.CharField(max_length=1)
    surplus = models.CharField(max_length=1)


class PTC_Information(models.Model):
    
    record = models.ForeignKey(to=MonthlyRecord, on_delete=models.CASCADE, related_name="ptcInfo")
    chairman = models.ForeignKey(CHAIRMAN, on_delete=models.SET_NULL, null=True)
    bank = models.ForeignKey(BANK, on_delete=models.SET_NULL, null=True)
    
    electionDate = models.DateField(verbose_name="PTC Election Date")
    estiblishDate = models.DateField(verbose_name="PTC Establish Date")
    areaCode =  models.PositiveBigIntegerField(verbose_name="Branc/Area/Code No")
    accountNo = models.CharField(max_length=10, verbose_name="Account No")
    lastYearAmount = models.PositiveBigIntegerField(verbose_name="Last Year Amount")
    consumed = models.PositiveBigIntegerField()
    prevRemainingBalance = models.PositiveBigIntegerField(verbose_name="Prev Balance")
    currentYearAmount = models.PositiveBigIntegerField(verbose_name="Current Year Amount")
    crcAllocation = models.PositiveBigIntegerField(verbose_name="CRC Allocation")
    pittyRepair = models.PositiveBigIntegerField(verbose_name="Pitty Repair")
    totalExpenditure = models.PositiveBigIntegerField(verbose_name="Total Expenditure")
    balance = models.PositiveBigIntegerField(verbose_name="Balance")
