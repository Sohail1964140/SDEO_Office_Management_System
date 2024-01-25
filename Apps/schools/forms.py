from .models import SCHOOL
from django import forms

class SchoolForm(forms.ModelForm):
    
    class Meta:
        model = SCHOOL
        fields = '__all__'
        
        widgets = {
            'name': forms.TextInput(attrs={'class':'maxlen'}),
            'ddo': forms.TextInput(attrs={'class':'maxlen'}),
            'yearOfConstruction': forms.DateInput(attrs={'class':'form-control'}),
            'uc' : forms.Select(attrs={'class':"sDD"}),
            'user': forms.Select(attrs={'class':'sDD'})
        }