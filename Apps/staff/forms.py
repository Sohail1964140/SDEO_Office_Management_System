from django import forms
from . models import (
                      TEACHER, CONTACT,
                      TeacherProffQualification, TeacherAccadQualification,
                      TeacherFirstAppointment, TeacherMonthlyEntry,
                      Transfer, Promotion
                      )
from Apps.schools.models import SCHOOL
from Apps.core.models import POST

class TeacherForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        
        isUpdte = False
        if 'isUpdate' in kwargs:
            isUpdte = True
            kwargs.pop('isUpdate')
        super().__init__(*args, **kwargs)
        
        if isUpdte:
            self.fields['dob'].widget = forms.DateInput(attrs={'type':"date" })
            self.fields['dateOfTakingOverChargeInPresentSchool'].widget = forms.DateInput(attrs={'type':"date" })
            self.fields['dateOfTakingOverChargeOnPresentPost'].widget = forms.DateInput(attrs={'type':"date" })

        
    
    class Meta:
        
        model = TEACHER
        fields = '__all__'
        
        widgets = {
            'image':forms.FileInput(attrs={'id':'myDropify', 'class':"border"}),
            'school':forms.Select(attrs={'class':"sDD"}),
            'post':forms.Select(attrs={'class':"sDD"}),
            'gender':forms.Select(attrs={'class':"sDD"}),
            'cnic': forms.TextInput(attrs={'data-inputmask-alias':"*****-*******-*"}),
            'name': forms.TextInput(attrs={'class':"maxlen", 'placeholder':'Enter your name'}),
            'fname': forms.TextInput(attrs={'class':"maxlen", 'placeholder':'Enter your father name'}),
            'dob': forms.TextInput(attrs={'class':"form-control", 'type':"text"}),
            'address': forms.Textarea(attrs={'class':"maxlen"}),
            'salary': forms.TextInput(attrs={'data-inputmask':"'alias': 'currency'"}),
            'dateOfTakingOverChargeInPresentSchool': forms.TextInput(attrs={'class':"form-control"}),
            'dateOfTakingOverChargeOnPresentPost': forms.TextInput(attrs={'class':"form-control"}),
        }
        
class TeacherContactForm(forms.ModelForm):
    
    class Meta:
        model = CONTACT
        
        fields = ['contact']
        widgets = {
            'contact': forms.TextInput(attrs={'class':'maxlen','data-inputmask-alias':"***********"})
        }
        

class TeacherProffQualificationForm(forms.ModelForm):
    
    class Meta:
        model = TeacherProffQualification
        
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class':'maxlen'})
        }

class TeacherAccadQualificationForm(forms.ModelForm):
    
    class Meta:
        model = TeacherAccadQualification
        
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class':'maxlen'})
        }

class TeacherFirstAppointmentForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
    
        isUpdte = False
        if 'isUpdate' in kwargs:
            isUpdte = True
            kwargs.pop('isUpdate')
        super().__init__(*args, **kwargs)
        
        if isUpdte:
            self.fields['dateOfFirstAppointment'].widget = forms.DateInput(attrs={'type':"date" })

    class Meta:
        model = TeacherFirstAppointment
        
        fields = ['appointmentPost', 'dateOfFirstAppointment']
        widgets = {
            'dateOfFirstAppointment': forms.TextInput(attrs={'class':"form-control"}),
            'appointmentPost':forms.Select(attrs={'class':"sDD"}),
            
        }




class TransferForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        
        personalNo = None
        if 'personalNo' in kwargs.keys():
            
            personalNo = kwargs.pop('personalNo')
            
        super().__init__(*args, **kwargs)
        

        
        if  personalNo is None:
            
            self.fields['toSchool'] = forms.ModelChoiceField(queryset=SCHOOL.objects.none(), blank=True, widget=forms.Select(attrs={ 'class':'sDD','id':"id_toSchool"}))
        else:
            teacher = TEACHER.totalTeachers.get(personal_no=personalNo)
            
            self.fields['toSchool'] = forms.ModelChoiceField(queryset=SCHOOL.objects.all().exclude(pk=teacher.school.pk), blank=True, widget=forms.Select(attrs={'class':'sDD','id':"id_toSchool"}))
            
    
    class Meta:
        
        
        
        model = Transfer
        fields = ['toSchool', 'date']

        widgets = {
            'date': forms.TextInput(attrs={'class':"form-control"}),
            
            
        }


class PromotionForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        
        personalNo = None
        if 'personalNo' in kwargs.keys():
            
            personalNo = kwargs.pop('personalNo')
            
        super().__init__(*args, **kwargs)
        
        if  personalNo is None:
            
            self.fields['toPost'] = forms.ModelChoiceField(queryset=POST.objects.none(),widget=forms.Select(attrs={}), label="To Post")
        else:
            teacher = TEACHER.totalTeachers.filter(personal_no=personalNo).first()
            
            if not teacher.post.bps == "13":
            
                 self.fields['toPost'] = forms.ModelChoiceField(queryset=POST.objects.all().exclude(pk=teacher.post.pk).exclude(bps="13"), widget=forms.Select(attrs={}),label="To Post")
            else:
                 self.fields['toPost'] = forms.ModelChoiceField(queryset=POST.objects.none(), widget=forms.Select(attrs={}),label="To Post")
                
    
    class Meta:
        
        
        
        model = Promotion
        fields = ['toPost', 'date']

        widgets = {
            'date': forms.TextInput(attrs={'class':"form-control"}),
        }


class TeacherMonthlyEntryForm(forms.ModelForm):
    
    class Meta:
        
        model = TeacherMonthlyEntry
        fields = ['teacher','school', 'post', 'salary', 'date']
        
        