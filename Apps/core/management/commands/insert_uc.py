from django.core.management.base import BaseCommand
from Apps.core.models import CIRCLE, UC
from faker import Faker

faker = Faker()

class Command(BaseCommand):
    
    help = "insert ucs for testing porpus"
    
    
    def handle(self, *args, **kwargs):
        
        circles = CIRCLE.objects.all()
        
        for circle in circles:
            
            for _ in range(50):
                
                name = faker.name()
                UC.objects.create(name=name, circle=circle)
                
        print("Uc is inserted succss fully")
    
