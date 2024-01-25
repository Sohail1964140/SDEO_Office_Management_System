from django.shortcuts import render, HttpResponse, get_object_or_404
from django.http import JsonResponse
from .forms import (TeacherForm, TeacherFirstAppointmentForm,
                    TeacherAccadQualificationForm, TeacherProffQualificationForm,
                    TeacherContactForm,
                    TransferForm,
                    PromotionForm
                    )
from .models import *
from Apps.core.models import UC, CIRCLE, POST, hx_Redirect
from Apps.schools.models import SCHOOL
from django.views import View
from django.views.generic import ListView
from django.contrib import messages
from django.http import Http404
from render_block import render_block_to_string
from django.core.paginator import Paginator
from django.contrib.auth.hashers import check_password
from django.db.models import Q
from django.db import transaction
import json
from time import sleep
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


def get_template(request, name,path="teacher"):
    
    template = f'{path}/{name}.html'
    
    if request.htmx:
        template  = f'{path}/partials/{name}.html'

    return template



"""
Teacher Create View
"""
class TeacherCreateView(LoginRequiredMixin,View):
    
    def get(self, request):
        
        context = {
            'form': TeacherForm(), 
            'appointmentForm': TeacherFirstAppointmentForm(),
            'accadForm': TeacherAccadQualificationForm(),
            'proffForm': TeacherProffQualificationForm(),
            'contactForm': TeacherContactForm(),
            'heading':'Add New Teacher'
            }
        
        
        template = get_template(request, 'teacher_add')
        return render(request, template, context)
    
    
    def post(self, request):
        
        appdata = {
                    'dateOfFirstAppointment': request.POST.get("dateOfFirstAppointment"),
                    'appointmentPost': request.POST.get("appointmentPost"),
                   
                   }
        
        form = TeacherForm(data=request.POST, files=request.FILES)
        
        
        appForm = TeacherFirstAppointmentForm(data=appdata)
        teacher = None
        if form.is_valid() and appForm.is_valid():
            
            teacher = form.save()
            appointement = appForm.save(commit=False)
            appointement.teacher = teacher
            appointement.save()
            messages.success(request, f"{teacher} added successfully")
            # form = TeacherForm()
            # appForm = TeacherFirstAppointmentForm()
            
            request.session['teacher'] = teacher.pk
        else:
            messages.error(request, "Please correct the Error Bellow")
        
        context = {
            
            'form': form,
            'appointmentForm': appForm,
            'accadForm': TeacherAccadQualificationForm(),
            'proffForm': TeacherProffQualificationForm(),
            'contactForm': TeacherContactForm(),
            'isSubmit': True,
            'object': teacher
            }
        
        template_name = get_template(request, 'teacher_add')
        return render(request,template_name, context)


"""
Teacher List View
"""
class TeacherListView(LoginRequiredMixin,ListView):
    
    model = TEACHER
    context_object_name = 'teachers'
    paginate_by = 10
    paginate_orphans = 2
    
    def get_template_names(self): return get_template(self.request, 'teacher_list')
    
    
    def paginate_queryset(self, queryset, page_size):
        
        try:
            
            return super(TeacherListView, self).paginate_queryset(queryset, page_size)
        except Http404:
            
            self.kwargs['page'] = 1
            return super(TeacherListView, self).paginate_queryset(queryset, page_size)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ucs'] = UC.objects.all().order_by('pk')
        context['schools'] = SCHOOL.objects.all().order_by('pk')
        context['circles']  = CIRCLE.objects.all().order_by('pk')
        context["isSearch"] = False
        return context



    
"""
TEACHER UPDATE VIEW
"""

class TeacherUpdateView(LoginRequiredMixin,View):
    
    
    def get(self, request, pk):
        
        
        teacher = get_object_or_404(TEACHER, pk=pk)
        teacherFirstAppointment = TeacherFirstAppointment.objects.get(teacher=teacher)
        form = TeacherForm(instance=teacher, isUpdate=True)
        
        template_name = get_template(request, 'teacher_add')
        request.session['teacher'] = teacher.pk
        context = {
            
            'form':form,
            'appointmentForm':TeacherFirstAppointmentForm(instance=teacherFirstAppointment, isUpdate=True),
            'heading':'Update Teacher','isUpdate':True, 
            'object': teacher,
            'contacts': teacher.contacts.all(),
            'proffQs': teacher.Proffqualification.all(),
            'accadQs': teacher.Accadqualification.all(),
            'isList':True,
            'isSubmit': True,
            
            }
        return render(request, template_name, context)
    
    def post(self, request, pk):
        
        
        appdata = {
            'dateOfFirstAppointment': request.POST.get("dateOfFirstAppointment"),
            'appointmentPost': request.POST.get("appointmentPost"),
        
        }
        
        teacher = get_object_or_404(TEACHER, pk=pk)
        teacherFirstAppointment = TeacherFirstAppointment.objects.get(teacher=teacher)
        form = TeacherForm(instance=teacher, data=request.POST, files=request.FILES)
        template_name = get_template(request, 'teacher_add')
        
        appForm = TeacherFirstAppointmentForm(instance=teacherFirstAppointment,data=appdata)
        
        if form.is_valid() and appForm.is_valid():
            
            teacher = form.save()
            appointement = appForm.save(commit=False)
            appointement.teacher = teacher
            appointement.save()
            messages.success(request, f"{teacher} Updated successfully")
            
        else:
            messages.error(request, 'Please correct the Error Bellow')
        
        
        context = {
            'form':form,
            'appointmentForm':TeacherFirstAppointmentForm(instance=teacherFirstAppointment),
            'heading':'Update Teacher','isUpdate':True, 
            'object': teacher,
            'contacts': teacher.contacts.all(),
            'proffQs': teacher.Proffqualification.all(),
            'accadQs': teacher.Accadqualification.all(),
            'isList':True,
            'isSubmit': True,
            'isUpdate': True
            }
        
        return render(request, template_name, context)


"""
TEACHER SEARCH VIEW
"""
class TeacherSearchView(LoginRequiredMixin,View):
    
    
    def get(self, request):
        
        page_number = request.GET.get('page', 1)
        query = json.loads(request.GET.get('query'))
        
        teachers = TEACHER.objects.all()
        
        if query.get("search"):
            teachers = teachers.filter(
                Q(name__istartswith=query.get('search')) | Q(personal_no=query.get('search'))|
                Q(cnic__istartswith=query.get('search')) | Q(address__istartswith=query.get('search'))
                )
        
        if query.get("circle"):
            circle = CIRCLE.objects.get(pk=query.get("circle"))
            teachers = teachers.filter(school__uc__circle=circle)
        
        if query.get("uc"):
            uc = UC.objects.get(pk=query.get("uc"))
            teachers = teachers.filter(school__uc=uc)
            
        if query.get("school"):
            school = SCHOOL.objects.get(pk=query.get("school"))
            teachers = teachers.filter(school=school)
            
        paginator = Paginator(teachers.order_by('pk'), per_page=10)
        
        page = paginator.get_page(page_number)

        context={
            
            'teachers': page.object_list,
            'page_obj': page,
            'isSearch': True,
            'request':request
        }
        
        response = render_block_to_string('teacher/partials/teacher_list.html', 'table', context)
        return HttpResponse(response)
    
    

    
"""
TEACHER DELETE VIEW
"""
class TeacherDeleteView(LoginRequiredMixin,View):
    
    
    def get(self, request, pk):
       
        try:
            teacher = get_object_or_404(TEACHER, pk=pk)
            
            context = {'object': teacher, 'msg': f'Are you sure you want to delete  <strong> <i>{teacher.name}</i></strong>? This action cannot be undone.'}
            
            template_name = get_template(request, 'teacher_delete')
            return render(request, template_name, context)
        

        except Http404:
            
            
            return render(request, 'utils/404.html') 
    
    
    
    def post(self, request, pk):
        
        
        email = request.POST.get('email')
        password = request.POST.get('password')
        personalNo = request.POST.get('personalNo')
        template_name = get_template(request, 'teacher_delete')
        user = request.user
        teacher = get_object_or_404(TEACHER, pk=pk)
        
        
        if user.email == email:
            
            if check_password(password, user.password):
                
                if teacher.personal_no == personalNo:
                    
                    teacher.delete()
                    messages.success(request, f'{teacher.name} deleted successfully')

                    context = {'isDeleted': True,'msg': f'{teacher.name} deleted Successfully'}
                    return render(request, template_name, context)
        
        
        messages.warning(request, "To ensure the security, please fill the given information")
        
        context = {
            'object':teacher,
            'msg': 'Please ensure that all information is entered correctly before submitting the form <br> Your security is our top priority'
                   
                   }
        return render(request, template_name, context)


@login_required
def deleteForm(request):
    return HttpResponse("")

# Proffitional Qualification views

class ProffQualificationView(LoginRequiredMixin,View):
    
    def get(self, request):
        
        data = {
            'proffForm': TeacherProffQualificationForm(),
        }
        return render(request, 'teacher/partials/proffQualification.html', data)
    
    def post(self, request):
        
        pQ = None
        islist = False
        form = TeacherProffQualificationForm(request.POST)
        
        if 'teacher' in request.session.keys():
            
            teacher = TEACHER.objects.get(pk=request.session.get('teacher'))
            
            if form.is_valid():
                
                try:
                    pQ = form.save(commit=False)
                    pQ.teacher = teacher
                    pQ.save()
                    islist = True
                except:
                    islist = False
                    
        data = {
            'pQ': pQ,
            'isList': islist,
            'proffForm': form
        }
        return render(request, 'teacher/partials/proffQualification.html', data)
    

@login_required
def deleteProffQ(request, pk):
    TeacherProffQualification.objects.get(pk=pk).delete()
    return HttpResponse("")


# Accademic Qualification views

class AccadQualificationView(LoginRequiredMixin,View):
    
    def get(self, request):
        
        data = {
            'accadForm': TeacherAccadQualificationForm(),
        }
        return render(request, 'teacher/partials/accadQualification.html', data)
    
    def post(self, request):
        
        aQ = None
        islist = False
        form = TeacherAccadQualificationForm(request.POST)
        
        if 'teacher' in request.session.keys():
            
            teacher = TEACHER.objects.get(pk=request.session.get('teacher'))
            
            if form.is_valid():
                
                try:
                    aQ = form.save(commit=False)
                    aQ.teacher = teacher
                    aQ.save()
                    islist = True
                except:
                    islist = False
                    
        data = {
            'aQ': aQ,
            'isList': islist,
            'accadForm': form
        }
        return render(request, 'teacher/partials/accadQualification.html', data)
    

@login_required
def deleteAccadQ(request, pk):
    TeacherAccadQualification.objects.get(pk=pk).delete()
    return HttpResponse("")



# Contact views

class ContactView(LoginRequiredMixin,View):
    
    def get(self, request):
        
        data = {
            'contactForm': TeacherContactForm(),
        }
        return render(request, 'teacher/partials/contact.html', data)
    
    def post(self, request):
        
        contact = None
        islist = False
        form = TeacherContactForm(request.POST)
        
        if 'teacher' in request.session.keys():
            
            teacher = TEACHER.objects.get(pk=request.session.get('teacher'))
            
            if form.is_valid():
                
                try:
                    contact = form.save(commit=False)
                    contact.teacher = teacher
                    contact.save()
                    islist = True
                except:
                    islist = False
                    
        data = {
            'contact': contact,
            'isList': islist,
            'contactForm': form
        }
        return render(request, 'teacher/partials/contact.html', data)


@login_required
def deleteContact(request, pk):
    CONTACT.objects.get(pk=pk).delete()
    return HttpResponse("")




# Get Uc from  Circle
@login_required
def getUcsFromCircle(request):
    pk = request.GET.get('circleDD')
    if pk:
        circle = CIRCLE.objects.get(pk=pk)
        ucs = circle.UCs.all().order_by('pk')
    else:
        ucs = UC.objects.all()
    template = render_block_to_string('utils/dropDowns.html','ucBlock',{'ucs': ucs})

    return HttpResponse(template)

# Get School from Uc
@login_required
def getSchoolsFromUc(request):
    
    pk = request.GET.get('ucDD')
    if pk:
        uc = UC.objects.get(pk=pk)
        schools = uc.schools.all().order_by('pk')
    else:
        schools = SCHOOL.objects.all()
    template = render_block_to_string('utils/dropDowns.html','Schoolblock',{'schools': schools})

    return HttpResponse(template)


"""
=== ========= === ========= ===Teacher Transfer Views === ========= === ========= ===
"""
"""
Teacher Transfer Views
"""
class TransferAddView(LoginRequiredMixin,View):
    
    def get(self, request):
        
        template_name = get_template(request, name="transfer_add", path="transfer")
        context = {
            'heading': 'Teacher Transfer',
            'form': TransferForm(),
            'personalNos': TEACHER.objects.values_list('personal_no', flat=True)
        }
        return render(request,template_name, context)
    
    def post(self, request):
        
        personalNo = request.POST.get('personalNo')
        TransferToHigh = request.POST.get('TransferToHigh', False)
        template_name = get_template(request, name="transfer_add", path="transfer")
        personalNo = personalNo if personalNo else None

        
        
        form = TransferForm(data=request.POST, personalNo=personalNo)
        
        
        
        
        context = {'form': form, 'heading': 'Teacher Transfer',
                   'personalNos': TEACHER.objects.values_list('personal_no', flat=True),
                   'personalNo': str() if  personalNo is None else personalNo
                   }
        
        if personalNo is None:
            
            messages.error(request, "Personal No Required")
            
            return render(request,template_name, context)
        
        teacher = TEACHER.objects.filter(personal_no=personalNo)
        
        if not teacher.exists():
            messages.error(request, "Pease enter valid personal number")
            return render(request,template_name, context)
        
        teacher = teacher.first()
        fromSchool = teacher.school
        
 
        
        if TransferToHigh == 'on':
            with transaction.atomic():
                try:
                    Transfer.objects.create(
                        teacher=teacher,
                        fromSchool=fromSchool,
                        date = datetime.strptime(request.POST.get('date'), "%m/%d/%Y"),
                        toSchool = None
                    )
                    teacher.isInPrimarySchool = False
                    # teacher.school = None
                    teacher.save()
                    form = TransferForm(personalNo=personalNo)
                    messages.success(request, "Teacher is now transfer to High School")
                except:
                    messages.error(request, "There is  some issue while submitting the form")   
                
        elif form.is_valid():
            
            with transaction.atomic():
                try:
                    transfer = form.save(commit=False)
                    transfer.teacher = teacher
                    transfer.fromSchool = fromSchool
                    transfer.save()
                    # Change Teacher School To new School
                    teacher.school = transfer.toSchool
                    teacher.dateOfTakingOverChargeInPresentSchool = transfer.date
                    teacher.save()
                    form = TransferForm(personalNo=personalNo)
                    messages.success(request, "Teacher is now transfer to new School")
                except:
                    messages.error(request, "There is some issue while submitting the form")
        else:
            
            messages.error(request, "Please correct the errors bellow")
            
        

        context = {
            'form': form,
            'heading': 'Teacher Transfer',
            'personalNo':personalNo,
            'personalNos': TEACHER.objects.values_list('personal_no', flat=True),
            
            }
        return render(request,template_name, context)






"""
Teacher Transfer List View
"""
class TransferListView(LoginRequiredMixin,ListView):
    
    model = Transfer
    context_object_name = 'transfers'
    paginate_by = 10
    paginate_orphans = 2
    
    def get_template_names(self): return get_template(self.request, name='transfer_list', path="transfer")
    
    
    def paginate_queryset(self, queryset, page_size):
        
        try:
            
            return super(TransferListView, self).paginate_queryset(queryset, page_size)
        except Http404:
            
            self.kwargs['page'] = 1
            return super(TransferListView, self).paginate_queryset(queryset, page_size)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["isSearch"] = False
        context['personalNos'] = TEACHER.totalTeachers.values_list('personal_no', flat=True)
        return context



"""
TRANSFER SEARCH VIEW
"""
class TransferSearchView(LoginRequiredMixin,View):
    
    
    def get(self, request):
        
        page_number = request.GET.get('page', 1)
        query = request.GET.get('query')
        
        
        transfers = Transfer.objects.all()
        
        if query:
        
            transfers = transfers.filter(Q(teacher__personal_no=query))
        
    
            
        paginator = Paginator(transfers.order_by('pk'), per_page=10)
        
        page = paginator.get_page(page_number)

        context={
            
            'transfers': page.object_list,
            'page_obj': page,
            'isSearch': True,
            'request':request,
        }
        
        response = render_block_to_string('transfer/partials/transfer_list.html', 'table', context)
        return HttpResponse(response)
    
    
    
"""
Teacher Transfer Undo View
"""
@login_required
def TransferUndoView(request, pk):
    
    with transaction.atomic():
        try:
            
            transfer = Transfer.objects.get(pk=pk)
            teacher = transfer.teacher

            if teacher.isInPrimarySchool:
                teacher.school = transfer.fromSchool
                
                teacher.save()
            teacher.isInPrimarySchool = True
            # Reset date of taking overcharge in present school
            teacher.dateOfTakingOverChargeInPresentSchool = teacher.teacherRecords.all().filter(record__school=teacher.school).order_by('-pk').first().dateOfTakingOverChargeInPresentSchool
            teacher.save()
            transfer.delete()
            messages.success(request,"Operation done successfully")
        except:
            messages.error(request,"there is some error while submitting the form")
    

        return hx_Redirect("teacher:transferList")
    
    

@login_required
def checkPersonalNumberAndGetTransferSchool(request):
    
    personalNo = request.GET.get('personalNo')
    template_name = get_template(request, name='checkPersonalNumberAndGetTransferSchool', path='transfer')
    if not personalNo:
        
        context = {
            'msg':'Personal Number is required',
            'type':'danger',
            'schools': None
        }
        return render(request, template_name, context)
    
    teacher = TEACHER.objects.filter(personal_no=personalNo)
    
    if not teacher.exists():
        
        
        context = {
            'msg':"Teacher dosn't exist",
            'type':'danger',
            'schools': None
            }
        
        return render(request,template_name, context)
    
    teacher = teacher.first()
    
    context = {
        'msg':'',
        'type':'success',
        'schools': SCHOOL.objects.all().exclude(pk=teacher.school.pk)
    }
    
    return render(request,template_name, context)
    

"""
=== ========= === ========= ===Teacher Promotion Views === ========= === ========= ===
"""


"""
Teacher Promotion Views
"""
class PromotionAddView(LoginRequiredMixin,View):
    
    def get(self, request):
        
        template_name = get_template(request, name="promotion_add", path="promotion")
        context = {
            'heading': 'Teacher Promotion',
            'form': PromotionForm(),
            'personalNos': TEACHER.objects.values_list('personal_no', flat=True).exclude(post__bps="13")
        }
        return render(request,template_name, context)
    
    def post(self, request):
        
        personalNo = request.POST.get('personalNo')
        PromoteTo16 = request.POST.get('PromoteTo16', False)
        template_name = get_template(request, name="promotion_add", path="promotion")
        personalNo = personalNo if personalNo else None
        form = PromotionForm(data=request.POST, personalNo=personalNo)
        
        
        
        
        context = {'form': form, 'heading': 'Teacher Promotion',
                   'personalNos': TEACHER.objects.values_list('personal_no', flat=True).exclude(post__bps="13"),
                   'personalNo': str() if  personalNo is None else personalNo
                   }
        
        if personalNo is None:
            
            messages.error(request, "Personal No Required")
            
            return render(request,template_name, context)
        
        teacher = TEACHER.objects.filter(personal_no=personalNo)
        
        if not teacher.exists():
            messages.error(request, "Pease enter valid personal number")
            return render(request,template_name, context)
        
        teacher = teacher.first()
        fromPost = teacher.post
        
        
        
        
        if PromoteTo16 == 'on':
            
            with transaction.atomic():
                try:
                    promotion = Promotion.objects.create(
                    teacher=teacher,
                    fromPost = fromPost,
                    date = datetime.strptime(request.POST.get('date'), "%m/%d/%Y"),

                    )
                    teacher.isInPrimarySchool = False
                    teacher.save()
                    form = PromotionForm(personalNo=personalNo)
                    messages.success(request, "Teacher is now Promote to new Post")
                except:
                    messages.error(request, "There is  some issue while submitting the form")   
        elif form.is_valid():
            
            with transaction.atomic():
                try:
                    promotion = form.save(commit=False)
                    promotion.teacher = teacher
                    promotion.fromPost = fromPost
                    promotion.save()
                    # Change Teacher School To new School
                    teacher.post = promotion.toPost
                    teacher.dateOfTakingOverChargeOnPresentPost = promotion.date
                    teacher.save()
                    form = PromotionForm(personalNo=personalNo)
                    messages.success(request, "Teacher is now Promot to new Post")
                except:
                    messages.error(request, "There is some issue while sumbmitting the form")
        else:
            
            messages.error(request, "Please correct the errors bellow")
            
            
        

        context = {
            'form': form,
            'heading': 'Teacher Promotion',
            'personalNo':personalNo,
            'personalNos': TEACHER.objects.values_list('personal_no', flat=True).exclude(post__bps="13"),
            
            }
        return render(request,template_name, context)



"""
Teacher Transfer List View
"""
class PromotionsListView(LoginRequiredMixin,ListView):
    
    model = Promotion
    context_object_name = 'promotions'
    paginate_by = 10
    paginate_orphans = 2
    
    def get_template_names(self): return get_template(self.request, name='promotion_list', path="promotion")
    
    
    def paginate_queryset(self, queryset, page_size):
        
        try:
            
            return super(PromotionsListView, self).paginate_queryset(queryset, page_size)
        except Http404:
            
            self.kwargs['page'] = 1
            return super(PromotionsListView, self).paginate_queryset(queryset, page_size)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["isSearch"] = False
        context['personalNos'] = TEACHER.objects.values_list('personal_no', flat=True).exclude(post__bps="13")
        return context


"""
Teacher Promotion Search View
"""
class PromotionSearchView(LoginRequiredMixin,View):
    
    
    def get(self, request):
        
        page_number = request.GET.get('page', 1)
        query = request.GET.get('query')
        
        promotions = Promotion.objects.all()
        
        if query:
            promotions = promotions.filter(Q(teacher__personal_no=query))
        
    
            
        paginator = Paginator(promotions.order_by('pk'), per_page=10)
        
        page = paginator.get_page(page_number)

        context={
            
            'promotions': page.object_list,
            'page_obj': page,
            'isSearch': True,
            'request':request
        }
        
        response = render_block_to_string('promotion/partials/promotion_list.html', 'table', context)
        return HttpResponse(response)
    
   
"""
Teacher Promotion Undo View
"""
@login_required
def PromotionUndoView(request, pk):
    
    with transaction.atomic():
        try:
            promotion = Promotion.objects.get(pk=pk)
            teacher = promotion.teacher

            if teacher.isInPrimarySchool:
                teacher.post = promotion.toPost
                teacher.save()
                
            teacher.isInPrimarySchool = True
            teacher.dateOfTakingOverChargeOnPresentPost = teacher.teacherRecords.all().filter(record__school=teacher.school, post=teacher.post).order_by('-pk').first().dateOfTakingOverChargeOnPresentPost
            teacher.save()
            promotion.delete()
            messages.success(request,"Operation done successfully")
        except:
            messages.error(request,"there is some error while submitting the form")
    

        return hx_Redirect("teacher:promotionList")

@login_required
def checkPersonalNumberAndGetPromotionPost(request):
    
    personalNo = request.GET.get('personalNo')
    template_name = get_template(request, name='checkPersonalNumberAndGetPromotionPost', path='promotion')
    if not personalNo:
        
        context = {
            'msg':'Personal Number is required',
            'type':'danger',
            'posts': None
        }
        return render(request, template_name, context)
    
    teacher = TEACHER.objects.filter(personal_no=personalNo)
    
    if not teacher.exists():
        
        
        context = {
            'msg':"Teacher dosn't exist",
            'type':'danger',
            'posts': None
            }
        
        return render(request,template_name, context)
    
    teacher = teacher.first()
    
    context = {
        'msg':'',
        'type':'success',
        'posts':POST.objects.all().exclude(pk=teacher.post.pk).exclude(bps="13")
    }
    
    if  teacher.post.bps == "13":
        context['posts'] = None

        context['msg'] = "13 scale nerver promot"
        context['type'] ="danger"
    return render(request,template_name, context)
    
