from .models import ITEM_CATEGORY
from django.shortcuts import render, HttpResponse, get_object_or_404
from django.views.generic import CreateView, ListView, UpdateView
from .forms import ItemCategoryForm
from django.contrib import messages
from django.http import Http404
from django.core.paginator import Paginator
from django.views import View
from render_block import render_block_to_string
from django.contrib.auth.hashers import check_password
from django.contrib.auth.mixins import LoginRequiredMixin
"""
Creating New Item Category
"""
class ItemCategorAddView(LoginRequiredMixin,CreateView):
    
    model = ITEM_CATEGORY
    form_class = ItemCategoryForm
    
    template_name = "core/item_category/itemCategory_add.html"
    
    
    def get_template_names(self):
        
        if self.request.htmx:
            
            self.template_name="core/item_category/partials/itemCategory_add.html"
        
        return self.template_name
    
    def get_success_url(self):return None
    
    def post(self, request, *args, **kwargs):
        
        
        form = ItemCategoryForm(data=request.POST)
        
        if form.is_valid():
            
            cat = form.save()
            messages.success(self.request, "New Category Added")
            form = self.form_class
        else:
            
            messages.error(self.request, "Please Correct The Error Bellow")
        
        return render(request, self.get_template_names(), {'form': form}) 
        
        
    def form_valid(self, form):
        
        messages.success(self.request, "New Category Added")
        return super(ItemCategorAddView, self).form_valid(form)
    
    def form_invalid(self, form):
        

        return super(ItemCategorAddView, self).form_invalid(form)


"""
List All  Category
"""
class ItemCategoryList(LoginRequiredMixin,ListView):
    
    model = ITEM_CATEGORY
    template_name = "core/item_category/itemCategory_list.html"
    context_object_name = "ItemCategorys"
    
    paginate_by = 10
    
    def get_template_names(self):
        
        if self.request.htmx:
            
            self.template_name="core/item_category/partials/itemCategory_list.html"
        
        return self.template_name
    
    def get_queryset(self):
        
        return ITEM_CATEGORY.objects.all().order_by('pk')
    
    
    def paginate_queryset(self, queryset, page_size):
        
        try:
            
            return super(ItemCategoryList, self).paginate_queryset(queryset, page_size)
        
        except Http404:
            
            self.kwargs['page'] = 1
            return super(ItemCategoryList, self).paginate_queryset(queryset, page_size)
    



"""
Search All  Category
"""

class itemCategorySearchView(LoginRequiredMixin,View):
    
    def get(self, request):
        
        query = request.GET.get('query')
        page_number = request.GET.get('page', 1)
        
        categorys = ITEM_CATEGORY.objects.filter(name__istartswith=query)
        paginator = Paginator(categorys, per_page=10)
        
        page = paginator.get_page(number=page_number)
        
        context={
            'ItemCategorys':page.object_list,
            'isSearch':True,
            'page_obj': page,
            'request':request
        }
        
        response =  render_block_to_string('core/item_category/partials/itemCategory_list.html','table', context)
        
        return HttpResponse(response)




"""
Update  Item Category
"""
class ItemCategorUpdateView(LoginRequiredMixin,View):
    
    template_name = "core/item_category/itemCategory_add.html"
    
    def get_template(self):
        
        if self.request.htmx:
            self.template_name = 'core/item_category/partials/itemCategory_add.html'
            
        return self.template_name
    
    def get_object(self, name):
        obj = get_object_or_404(ITEM_CATEGORY, name=name)
        return obj
    
    def get(self, request, name):
        
        form = ItemCategoryForm(instance=self.get_object(name=name))
        
        context = {
            'isUpdate':True,
            'heading': "Update Item Category",
            'form': form,       
            'object': self.get_object(name=name)    
                   }
        return render(request, self.get_template(), context)
    
    def post(self, request, name):
        
        cate = self.get_object(name=name)
        form = ItemCategoryForm(instance=cate, data=request.POST)
        
        if form.is_valid():
            
            cate = form.save()
            messages.success(request, f"{cate} Updated")
            form = ItemCategoryForm(instance=cate)
            
        else:
            messages.error(request, "Please Correct the errors bellow")
            
        context = {
            'isUpdate':True,
            'heading': "Update Item Category",
            'form': form,       
            'object': cate    
                   }

        return render(request, self.get_template(), context)
    



"""
Delete  Item Category
"""

class itemCategoryDeleteView(LoginRequiredMixin,View):
    
    template_name = "core/item_category/delete.html"
    def get_template(self):
        
        if self.request.htmx:
            
            self.template_name = "core/item_category/partials/delete.html"
        return self.template_name

    def get_object(self):
        return get_object_or_404(ITEM_CATEGORY, name=self.kwargs['name'])

    
    def get(self, request, name):
       
        try:
            
            
            category = self.get_object()
            
            context = {'object': category, 'msg': f'Are you sure you want to delete  <strong> <i>{category.name}</i></strong>? This action cannot be undone.'}
            
            
            return render(request, self.get_template(), context)
        

        except Http404:
            
            return render(request, 'utils/404.html') 
    
    
    
    def post(self, request, name):
        
        
        email = request.POST.get('email')
        password = request.POST.get('password')
        input_name = request.POST.get('name')
        
        
        user = request.user
        category = self.get_object()
        if user.email == email:
            
            if check_password(password, user.password):
                
                if name == input_name:
                    
                    category.delete()
                    messages.success(request, f'{category.name} deleted successfully')

                    context = {'isDeleted': True,'msg': f'{category.name} deleted Successfully'}
                    return render(request,self.get_template(), context)
        
        
        messages.warning(request, "To ensure the security, please fill the given information")
        
        context = {
            'object':category,
            'msg': 'Please ensure that all information is entered correctly before submitting the form <br> Your security is our top priority'
                   
                   }
        return render(request, self.get_template(), context)
    