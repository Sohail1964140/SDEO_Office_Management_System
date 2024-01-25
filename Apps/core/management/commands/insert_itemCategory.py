from django.core.management.base import BaseCommand
from Apps.core.models import ITEM_CATEGORY
from faker import Faker
faker = Faker()



class Command(BaseCommand):
    
    help = "insert Item Category"
    
    def handle(self, *args, **kwargs):
        
        
        ITEM_CATEGORY.objects.all().delete()
        
        for _ in range(500):
            
            name =  faker.name()
            ITEM_CATEGORY.objects.create(name=name)
        
        
        
        print("Item Category Created Successfully")