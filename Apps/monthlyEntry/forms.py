from django import forms
from .models import (SchoolBuilding , SchoolStock, 
                     StaffAvalibility, TeacherMonthlyEntry,
                     StudentStrength,
                     MonthlyRecord,
                     PTC_Information
                     )

from Apps.core.models import YesNo,POST, CLASS_CHOICES, STOCK_ITEM
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_forms.bootstrap import InlineRadios, InlineCheckboxes
from django.urls import reverse_lazy as _



class SchoolBuildingForm(forms.ModelForm):
    
    
    computerLaboratory = forms.ChoiceField(choices=YesNo,  widget=forms.RadioSelect, initial=False)
    


    
    class Meta:
        model = SchoolBuilding
        fields = '__all__'
        exclude  = ['record']
        
        widgets = {
            'yearOfConstruction': forms.TextInput(attrs={'class':'form-control'}),
            'playGroud': forms.RadioSelect(attrs={'class':'form-check'}),
            'noOfClassRooms': forms.TextInput(attrs={'class':'maxlen'}),
            'noOfOtherRooms': forms.TextInput(attrs={'class':'maxlen'}),
            'coverdArea': forms.TextInput(attrs={'class':'maxlen'}),
            'uncoverdArea': forms.TextInput(attrs={'class':'maxlen'}),
            'noOfToilets': forms.TextInput(attrs={'class':'maxlen'}),
            'fruitTrees': forms.TextInput(attrs={'class':'maxlen'}),
            'shadyTrees': forms.TextInput(attrs={'class':'maxlen'}),
        }
        

class SchoolStockForm(forms.ModelForm):
    
    
    def __init__(self, *args, **kwargs):
    
        record = None
        if 'record' in kwargs:
            record = kwargs.pop('record')
        
        super().__init__(*args, **kwargs)
        
        if record:
            enterItems = SchoolStock.objects.filter(record__pk=record).values_list('item')
            
            self.fields['item'] = forms.ModelChoiceField(queryset= STOCK_ITEM.objects.exclude(pk__in=enterItems),
                                                         widget=forms.Select(attrs={}))
            
        
    class Meta:
        model = SchoolStock
        
        fields = '__all__'
        exclude  = ['record']
        widgets = {
            
            'noOfItems': forms.TextInput(attrs={'class':'maxlen'}),
            'required': forms.TextInput(attrs={'class':'maxlen'}),
            'surplus': forms.TextInput(attrs={'class':'maxlen'})
            
        }


class StaffAvalibilityForm(forms.ModelForm):
    
    
    def __init__(self, *args, **kwargs):
        
        record = None
        if 'record' in kwargs:
            
            record = kwargs.pop('record')
        
        super(StaffAvalibilityForm,self).__init__(*args, **kwargs)

        if record is not None:
            
            record = MonthlyRecord.objects.get(pk=record)
            
            staff_posts = StaffAvalibility.objects.filter(record=record).values_list('post',flat=True)


            self.fields['post']= forms.ModelChoiceField(queryset=POST.objects.all().exclude(pk__in=staff_posts), 
                                  widget=forms.Select(attrs={'hx-get':_('entry:getFilledStaff'),
                                        'hx-target':"#bom",
                                        })) 
            
            
    class Meta:
        model = StaffAvalibility
        
        fields = '__all__'
        exclude  = ['record']
        widgets = {
            'post': forms.Select(attrs={'hx-get':_('entry:getFilledStaff'),
                                        'hx-target':"#bom",
                                        }),
            'sanctioned': forms.TextInput(attrs={'class':'maxlen'}),
            'surplus': forms.TextInput(attrs={'class':'maxlen'}),
            'filled': forms.TextInput(attrs={'class':'maxlen','readonly':True})
            
        }
        
    



class TeacherMonthlyEntryForm(forms.ModelForm):
    
    class Meta:
        model = TeacherMonthlyEntry
        
        fields = '__all__'
        exclude  = ['record']
        widgets = {
            
            'salary': forms.TextInput(attrs={'class':'maxlen'}),
            'teacher': forms.Select(attrs={'class':''})
            
        }



class StudentStrengthEntryForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        
        record = None
        if 'record' in kwargs:
            record = kwargs.pop('record')
        
        super().__init__(*args, **kwargs)
        
        if record:
            
            strengthClasses = list(StudentStrength.objects.filter(record__pk=record).values_list('classID', flat=True))
            selectedClasses = [x for x in CLASS_CHOICES if x[0] not in strengthClasses]
            self.fields['classID'] = forms.ChoiceField(choices=selectedClasses, widget=forms.Select(attrs={'class':'form-control'}))
            

        
    class Meta:
        model = StudentStrength
        
        fields = '__all__'
        exclude  = ['record']
        widgets = {
            
            'boys':  forms.TextInput(attrs={'class':'maxlen'}),
            'girls': forms.TextInput(attrs={'class':'maxlen'})
            
        }
        

class PTC_InformationForm(forms.ModelForm):
    
    class Meta:
        model = PTC_Information
        fields = '__all__'
        exclude = ['record']
        widgets = {
            
            'accountNo':  forms.TextInput(attrs={'class':'maxlen'}),
            'electionDate': forms.TextInput(attrs={'class':'form-control'}),
            'estiblishDate': forms.TextInput(attrs={'class':'form-control'}),
        }