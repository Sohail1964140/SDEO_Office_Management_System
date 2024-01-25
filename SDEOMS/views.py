from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from Apps.core.models import CIRCLE, POST, UC
from Apps.schools.models import SCHOOL
from Apps.staff.models import TEACHER
from Apps.monthlyEntry.models import MonthlyRecord
from datetime import datetime
from render_block import render_block_to_string



@method_decorator(login_required, name="dispatch")
class HomeView(View):
    
    def get(self, request):
        
        try:
            if request.user.is_superuser:
                
                context = dict()
                
                context['circles'] = CIRCLE.objects.all().order_by("pk")
                context['ucs'] = UC.objects.all().order_by("pk")
                context['posts'] = POST.objects.all().order_by("pk")
                context['schools'] = SCHOOL.objects.all().order_by("pk")
                context['teachers'] = TEACHER.objects.all().count()
                context['addeds'] = [school for  school in  MonthlyRecord.objects.filter(date__year=datetime.today().year,date__month=datetime.today().month )]
                context['dark'] = request.session.get('dark', True)
                return render(request, "base.html", context)
            
            school = request.user.school or None
            return redirect(reverse_lazy("school:schoolProfile", kwargs={'slug':school.slug}))
        except:
            
            return render(request, "accounts/error/404.html")





def changeToDark(request):
    
    request.session['dark'] = True
    return redirect("home")

def changeToLight(request):
    
    request.session['dark'] = False
    
    return redirect("home")

def searchSchool(request):
    
    emis = request.GET.get("emis", False)
    data = dict()
    data['schools'] = SCHOOL.objects.filter(emis=emis) if emis else SCHOOL.objects.all()
    
    
    
    template = render_block_to_string("includes/dashboard.html", block_name="allSchool", context=data)
    
    return HttpResponse(template)