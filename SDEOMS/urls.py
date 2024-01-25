from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('', views.HomeView.as_view(), name="home"),
    path('core/', include('Apps.core.urls', namespace='core')),
    path('school/', include('Apps.schools.urls', namespace='school')),
    path('teacher/', include('Apps.staff.urls', namespace='staff')),
    path('entry/', include('Apps.monthlyEntry.urls', namespace='entry')),
    path('reports/', include('Apps.Reports.urls', namespace='reports')),
    path('account/', include('allauth.urls')),
    # Extra
    path('get/school/', views.searchSchool, name="searchSchool"),
    path('dark/', views.changeToDark, name="changeToDark"),
    path('light/', views.changeToLight, name="changeToLight"),
] 


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
