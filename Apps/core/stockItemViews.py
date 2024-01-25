from .forms import stockItemForm
from .models import ITEM_CATEGORY, STOCK_ITEM
from django.shortcuts import render, HttpResponse
from django.views.generic import ListView, CreateView
from django.http import Http404
from django.contrib import messages
from django.views import View
from django.core.paginator import Paginator
from render_block import render_block_to_string
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import check_password
import json
from time import sleep
from django.contrib.auth.mixins import LoginRequiredMixin

"""
STOCK ITEM CREATE VIEW
"""
class StockItemCreateView(LoginRequiredMixin,CreateView):
    
    model = STOCK_ITEM
    template_name = "core/stock_item/stockItem_add.html"
    form_class = stockItemForm
    
    def get_template_names(self):
        
        if self.request.htmx:
            self.template_name="core/stock_item/partials/stockItem_add.html"

        return self.template_name
    
    def get_success_url(self): return None

    def get_context_data(self):
        
        context = super(StockItemCreateView, self).get_context_data()
        context['heading'] = "Add New Sotck Item"
        return context
    
    def post(self, request, *args, **kwargs):
        
        form = self.form_class(data=request.POST)
        
        if form.is_valid():
            
            uc = form.save()
            messages.success(request, f"New Stock Item `{uc}` Added Successfully")
            self.template_name = self.get_template_names()
            context = {'heading':'Add New Stock Item', 'form': self.form_class}
            return render(request, self.template_name, context)
        
        messages.error(request, "Please correct error bellow")
        self.template_name = self.get_template_names()
        context = {'heading':'Add New Stock Item', 'form': form}
        return render(request, self.template_name, context)
    
    
    
    
"""
STOCK ITEM LIST VIEW
"""
class StockItemListView(LoginRequiredMixin,ListView):
    
    model = STOCK_ITEM
    template_name = "core/stock_item/stockItem_list.html"
    context_object_name = 'items'
    paginate_by = 10
    paginate_orphans = 2
    
    def get_template_names(self):
        if self.request.htmx:
            
            self.template_name="core/stock_item/partials/stockItem_list.html"
        
        return self.template_name
    
    def get_queryset(self):
        return STOCK_ITEM.objects.all().order_by('pk')
    
    def paginate_queryset(self, queryset, page_size):
        
        try:
            
            return super(StockItemListView, self).paginate_queryset(queryset, page_size)
        except Http404:
            
            self.kwargs['page'] = 1
            return super(StockItemListView, self).paginate_queryset(queryset, page_size)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["isSearch"] = False
        context['categorys'] = ITEM_CATEGORY.objects.all().order_by('pk')
        return context
    
    
"""
SEARCH STOCK ITEM VIEW
"""

class stockItemSearch(LoginRequiredMixin,View):
    
    
    def get(self, request):
        

        page_number = request.GET.get('page', 1)
        query = json.loads(request.GET.get('query'))
        
        items = STOCK_ITEM.objects.all()
        if query.get("search"):
            
            items = items.filter(name__istartswith=query.get('search'))
        
        if query.get("category"):
            
            category = ITEM_CATEGORY.objects.get(pk=query.get('category'))
            
            items = items.filter(category=category)
        
        
        paginator = Paginator(items.order_by('pk'), per_page=10)
        
        page = paginator.get_page(page_number)

        context={
            
            'items': page.object_list,
            'page_obj': page,
            'isSearch': True,
            'categorys':ITEM_CATEGORY.objects.all().order_by('pk'),
            'request':request
        
        }
        
        response = render_block_to_string('core/stock_item/partials/stockItem_list.html', 'table', context)
        
        
        
        return HttpResponse(response)
    


"""
STOCK ITEM UPDATE VIEW
"""

class stockItemUdateView(LoginRequiredMixin,View):
    
    template_name = "core/stock_item/stockItem_add.html"
   
    def get_template(self):
        
        if self.request.htmx:
            self.template_name="core/stock_item/partials/stockItem_add.html"
        
        return self.template_name
    
    def get_object(self):
        return get_object_or_404(STOCK_ITEM, name=self.kwargs['name'])
    
    def get(self, request, name):
        
        item = self.get_object()
        form = stockItemForm(instance=item)
        
        context = {'form':form, 'heading':'Update Sock Item','isUpdate':True, 'object': item}
        return render(request, self.get_template(), context)
    
    def post(self, request, name):
        
        item = self.get_object()
        form = stockItemForm(instance=item,data=request.POST)
        
        
        if form.is_valid():
            
            uc = form.save()
            messages.success(request, f'{item} Updated')
        else:
            messages.error(request, 'Please correct the Error Bellow')
        
        
        context = {'form':form, 'heading':'Update Stock Item','isUpdate':True, 'object': item}
        
        return render(request, self.get_template(), context)


"""
STOCK ITEM DELETE VIEW
"""

class stockItemDeleteView(LoginRequiredMixin,View):
    
    template_name = "core/stock_item/delete.html"
    def get_template(self):
        
        if self.request.htmx:
            self.template_name="core/stock_item/partials/delete.html"
        
        return self.template_name
    
    def get_object(self):
        
        return get_object_or_404(STOCK_ITEM, name=self.kwargs['name'])
    
    def get(self, request, name):
       
        try:
            item = self.get_object()
            
            context = {'object': item, 'msg': f'Are you sure you want to delete  <strong> <i>{item.name}</i></strong>? This action cannot be undone.'}
            
            
            return render(request, self.get_template(), context)
        

        except Http404:
            
            
            return render(request, 'utils/404.html') 
    
    
    
    def post(self, request, name):
        
        
        email = request.POST.get('email')
        password = request.POST.get('password')
        input_name = request.POST.get('name')
        user = request.user
        item = self.get_object()
    
        if user.email == email:
            
            if check_password(password, user.password):
                
                if name == input_name:
                    
                    item.delete()
                    messages.success(request, f'{item.name} deleted successfully')

                    context = {'isDeleted': True,'msg': f'{item.name} deleted Successfully'}
                    return render(request, self.get_template(), context)
        
        
        messages.warning(request, "To ensure the security, please fill the given information")
        
        context = {
            'object':item,
            'msg': 'Please ensure that all information is entered correctly before submitting the form <br> Your security is our top priority'
                   
                   }
        return render(request, self.get_template(), context)