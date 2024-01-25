from django.urls import path
from .views import *

app_name = "school"
urlpatterns = [    
    path('add/', SchoolCreateView.as_view(), name="schoolAdd"),
    path('list/', SchoolListView.as_view(), name="schoolList"),
    path('search/', SchoolSearchView.as_view(), name="schoolSearch"),
    path('update/<slug:slug>', SchoolUpdateView.as_view(), name="schoolUpdate"),
    path('delete/<slug:slug>', SchoolDeleteView.as_view(), name="schoolDelete"),
 
    # Profile
    path('<slug:slug>/profile/', SchoolProfilePage.as_view(), name="schoolProfile"),
    path('record/show/<int:pk>', get_Records, name="getRecord"),
    path('record/add/<int:pk>', add_Record, name="addRecord"),
    
]
