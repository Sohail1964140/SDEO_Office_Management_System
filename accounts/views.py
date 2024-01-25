from typing import Optional
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from Apps.core.models import hx_Redirect
from .forms import UserAuthenticationForm, UserForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View
from django.contrib import messages
from django.views.generic import ListView
from django.contrib.auth import get_user_model
import json
from django.db.models import Q
from render_block import render_block_to_string
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


def get_template(request, name):
    template_name = f"accounts/{name}.html"
    
    if request.htmx:
        template_name = f"accounts/partials/{name}.html"
    
    return template_name

# Create your views here.

class UserRegistrationView(LoginRequiredMixin,View):
    
    def get(self, request):
        form = UserForm()
        tempate_name =get_template(request, 'registration')
        
        return render(request,tempate_name , {'form': form})

    def post(self, request):
        
        form = UserForm(data=request.POST)
        tempate_name =get_template(request, 'registration')
        
        if form.is_valid():
            
            user = form.save(commit=False)
            user.is_staff = True
            user.save()
            messages.success(request, "User Created Successfully")
            
            return hx_Redirect("accounts:signup")
        
        messages.error(request, "Please correct the error bellow")
        return render(request,tempate_name , {'form': form})

class UserLoginView(LoginView):
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse_lazy('home'))  # Replace 'home' with the URL name of your home page
        return super().dispatch(request, *args, **kwargs)
    
    form_class = UserAuthenticationForm
    template_name = "accounts/login.html"


class UsersListView(LoginRequiredMixin,ListView):
    
    model = get_user_model()
    context_object_name = 'users'
    paginate_by = 10
    paginate_orphans = 2
    
    def get_template_names(self): return get_template(self.request, 'users')
    
    
    def paginate_queryset(self, queryset, page_size):
        
        try:
            
            return super(UsersListView, self).paginate_queryset(queryset, page_size)
        except Http404:
            
            self.kwargs['page'] = 1
            return super(UsersListView, self).paginate_queryset(queryset, page_size)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["isSearch"] = False
        return context
    
"""
USER SEARCH VIEW
"""
class UserSearchView(LoginRequiredMixin,View):
    
    
    def get(self, request):
        
        page_number = request.GET.get('page', 1)
        query = json.loads(request.GET.get('query'))
        
        users = get_user_model().objects.all()
        
        if query.get("search"):
            users = users.filter(
                Q(email__istartswith=query.get('search')))
        
        paginator = Paginator(users.order_by('pk'), per_page=10)
        
        page = paginator.get_page(page_number)

        context={
            
            'users': page.object_list,
            'page_obj': page,
            'isSearch': True,
        }
        
        response = render_block_to_string('accounts/partials/users.html', 'table', context)
        return HttpResponse(response)
    
    

# class UserLogoutView(LogoutView):
    
#     pass