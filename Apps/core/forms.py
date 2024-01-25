from django import forms
from .models import (CIRCLE, UC, ITEM_CATEGORY, STOCK_ITEM, POST, BANK, CHAIRMAN)
from crispy_forms.helper import FormHelper

"""
Circle Form
"""
class CircleForm(forms.ModelForm):
    
    
    
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_show_labels = True
        
        
    class Meta:
        
        model = CIRCLE
        
        fields = '__all__'
        
        
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control maxlen', 'placeholder':'Enter Name'})
        }
        



"""
Uc Form
"""

class UcForm(forms.ModelForm):
    
    class Meta:
        model = UC
        fields = '__all__'
        
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control maxlen'})
        }




"""
ItemCategory Form
"""

class ItemCategoryForm(forms.ModelForm):
    
    class Meta:
        model = ITEM_CATEGORY
        fields = '__all__'
        
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control maxlen'})
        }


"""
stockItem Form
"""
class stockItemForm(forms.ModelForm):
    
    class Meta:
        model = STOCK_ITEM
        fields = '__all__'
        
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control maxlen'})
        }


"""
POST Form
"""
class postForm(forms.ModelForm):
    
    class Meta:
        model = POST
        fields = '__all__'
        
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control maxlen'})
        }
        


"""
BANK Form
"""
class bankForm(forms.ModelForm):
    
    class Meta:
        model = BANK
        fields = '__all__'
        
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control maxlen'})
        }


"""
BANK Form
"""
class chairmanForm(forms.ModelForm):
    
    class Meta:
        model = CHAIRMAN
        fields = '__all__'
        
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control maxlen'}),
            'contact': forms.TextInput(attrs={'class':'form-control maxlen'}),
        }