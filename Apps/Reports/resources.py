from Apps.schools.models import SCHOOL
from Apps.staff.models import TEACHER
from import_export import resources, fields

class School_List(resources.ModelResource):
    uc = fields.Field(column_name="uc", attribute="uc__name")
    circle = fields.Field(column_name="circle", attribute="uc__circle")
    class Meta:
        model = SCHOOL
        
        fields = ['circle','uc','emis','name']
    

    def get_export_order(self):
        return [
            'emis','name','uc','circle'
        ]


class TEACHER_Govt_Election_Resource(resources.ModelResource):
    
    school = fields.Field(column_name="School", attribute="school__name")
    uc = fields.Field(column_name="UC", attribute="school__uc__name")
    circle = fields.Field(column_name="circle", attribute="school__uc__circle")
    post = fields.Field(column_name="Designation", attribute="post")
    contact = fields.Field(column_name="Contact", attribute="get_contact")
    
    class Meta:
        model = TEACHER
    
        fields = [
            'school', 'name', 'post', 'circle', 'uc', 'contact' 
        ]
        