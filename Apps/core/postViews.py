from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView
from .models import (POST,PBS_CHOICE)
from .forms import (postForm)
from django.contrib import messages
from django.http import Http404
from render_block import render_block_to_string
from django.core.paginator import Paginator
from django.contrib.auth.hashers import check_password
from django_htmx.http import trigger_client_event
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
import json
from time import sleep



def get_template(request, name):
    
    template_name = f'core/post/{name}'
    
    if request.htmx:
        template_name = f'core/post/partials/{name}'
    
    return template_name


"""
POST ADD VIEW
"""
class postCraeteView(LoginRequiredMixin,View):
    
    def get_template_names(self): return get_template(self.request, 'post_add.html')
    
    context = {'heading': 'Add New Post'}
    
    def get(self, request):
        
        self.context['form'] = postForm()
        return render(request,self.get_template_names(), self.context )
    
    def post(self, request):
        
        form = postForm(data=request.POST)
        
        if form.is_valid():
            
            post = form.save()
            messages.success(request, f"New Post {post} Added")
            form = postForm()
        
        else:
            
            messages.error(request,  "Please Correct The Error Bellow")
        
        self.context['form'] = form
        return render(request,self.get_template_names(), self.context)


"""
POST LIST VIEW
"""
class postListView(LoginRequiredMixin,ListView):
    
    model = POST
    context_object_name = 'posts'
    paginate_by = 10
    paginate_orphans = 2
    
    def get_template_names(self): return get_template(self.request, 'post_list.html')
    
    def get_queryset(self):
        return POST.objects.all()
    
    def paginate_queryset(self, queryset, page_size):
        
        try:
            
            return super(postListView, self).paginate_queryset(queryset, page_size)
        except Http404:
            
            self.kwargs['page'] = 1
            return super(postListView, self).paginate_queryset(queryset, page_size)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["isSearch"] = False
        context['scals'] = [s[0] for s in PBS_CHOICE]
        return context



"""
SEARCH POST VIEW
"""

class postSearchView(LoginRequiredMixin,View):
    
    
    def get(self, request):
        

        page_number = request.GET.get('page', 1)
        query = json.loads(request.GET.get('query'))
        
        posts = POST.objects.all()
        if query.get("search"):
            
            posts = posts.filter(name__istartswith=query.get('search'))
        
        if query.get("scale"):
                        
            posts = posts.filter(bps=query.get("scale"))
        
        
        paginator = Paginator(posts.order_by('pk'), per_page=10)
        
        page = paginator.get_page(page_number)

        context={
            
            'posts': page.object_list,
            'page_obj': page,
            'isSearch': True,
            'scals' : [s[0] for s in PBS_CHOICE],
            'request':request
        
        }
        
        response = render_block_to_string('core/post/partials/post_list.html', 'table', context)
        return HttpResponse(response)
    

"""
UPDATE POST VIEW
"""

class postUdateView(LoginRequiredMixin,View):


    def get_object(self):
        post = POST.objects.get(name=self.kwargs['name'], bps=self.kwargs['bps'])
        return post
    
    def get(self, request, name, bps):
        
        post = self.get_object()
        form = postForm(instance=post)
        
        context = {'form':form, 
                   'heading':'Update Post',
                   'isUpdate':True, 
                   'object': post
                   } 
        return render(request,get_template(request, 'post_add.html'), context)
    
    def post(self, request, name, bps):
        
        post = self.get_object()
        form = postForm(instance=post,data=request.POST)
        
        
        if form.is_valid():
            
            post = form.save()
            messages.success(request, f'{post} Updated')
        else:
            messages.error(request, 'Please correct the Error Bellow')
        
        
        context = {'form':form, 
                   'heading':'Update Post',
                   'isUpdate':True, 
                   'object': post
                   }
        
        return render(request, get_template(request, 'post_add.html'), context)



"""
POST DELETE VIEW
"""

class postDeleteView(LoginRequiredMixin,View):
    
    def get_object(self):  return  POST.objects.get(pk=self.kwargs['pk'])
    
    def get(self, request, pk):
       
        try:
            post = self.get_object()
            
            context = {'object': post, 
                       'msg': f'Are you sure you want to delete  <strong> <i>{post.name}</i></strong>? This action cannot be undone.',
                       'scals':[s[0] for s in PBS_CHOICE]
                       }
            
            
            return render(request,get_template(request, 'delete.html'), context)
        

        except Http404:
            
            
            return render(request, 'utils/404.html') 
    
    
    
    def post(self, request, pk):
        
        
        email = request.POST.get('email')
        password = request.POST.get('password')
        post_name = request.POST.get('name')
        post_scale = request.POST.get('scale')
        
        user = request.user
        post = self.get_object()
    
        if user.email == email:
            
            if check_password(password, user.password):
                
                if post.name == post_name and post.bps == post_scale:
                    
                    post.delete()
                    messages.success(request, f'{post.name} deleted successfully')

                    context = {
                                'isDeleted': True,
                                'msg': f'{post.name} deleted Successfully'
                               }
                    return render(request,get_template(request, 'delete.html'), context)
        
        
        messages.warning(request, "To ensure the security, please fill the given information")
        
        context = {
            'object':post,
            'msg': 'Please ensure that all information is entered correctly before submitting the form <br> Your security is our top priority'
                   
                   }
        return render(request, get_template(request, 'delete.html'), context)