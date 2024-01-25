from django.core.management.base import BaseCommand
from Apps.core.models import ITEM_CATEGORY, STOCK_ITEM
from faker import Faker
faker = Faker()



class Command(BaseCommand):
    
    help = "insert Item Category"
    
    def handle(self, *args, **kwargs):
        
        
        categorys = ITEM_CATEGORY.objects.all()
        
        for cat in categorys:
            
            for _ in range(100):
                
                name =  faker.name()
                STOCK_ITEM.objects.create(name=name,category=cat)
        
        
        
        print("Stock Item  Created Successfully")