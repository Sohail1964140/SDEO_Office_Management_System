from Apps.core.models import CIRCLE
from django.core.management.base import BaseCommand
from faker import Faker

faker = Faker()
class Command(BaseCommand):
    
    help = "Insert circle"
    
    
    def handle(self, *args, **options):
        
        
        
        for _ in range(500):
            
            name = faker.name()
            
            CIRCLE.objects.create(name=name)
        
        
        print("data inserted successfully")