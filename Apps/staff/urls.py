from django.urls import path
from .import views
app_name = "teacher"

urlpatterns = [
    path('add/', views.TeacherCreateView.as_view(), name="teacherAdd"),
    path('list/', views.TeacherListView.as_view(), name="teacherList"),
    path('update/<int:pk>/', views.TeacherUpdateView.as_view(), name="teacherUpdate"),
    path('delete/<int:pk>/', views.TeacherDeleteView.as_view(), name="teacherDelete"),
    path('search/', views.TeacherSearchView.as_view(), name="teacherSearch"),
    
    # filters
    path('load/uc/circle', views.getUcsFromCircle, name="getUcFromCircle"),
    path('load/school/uc', views.getSchoolsFromUc, name="getSchoolFromUc"),
    
    # partials urls
    path('proffQ/add/', views.ProffQualificationView.as_view(), name="proffQ"),
    path('proffQ/delete/<int:pk>/', views.deleteProffQ, name="proffQDelete"),
    path('form/delete/', views.deleteForm, name="deleteForm"),
    
    
    path('accadQ/add/', views.AccadQualificationView.as_view(), name="accadQ"),
    path('accadQ/delete/<int:pk>/', views.deleteAccadQ, name="accadQDelete"),
    
    path('contact/add/', views.ContactView.as_view(), name="contactAdd"),
    path('contact/delete/<int:pk>/', views.deleteContact, name="contactDelete"),
    
    # Transfer urls
    path('transfer/add/', views.TransferAddView.as_view(), name="transferAdd"),
    path('transfer/list/', views.TransferListView.as_view(), name="transferList"),
    path('transfer/search/', views.TransferSearchView.as_view(), name="transferSearch"),
    path('transfer/undo/<int:pk>', views.TransferUndoView, name="transferUndo"),
    path('checkPersonalNumberAndGetTransferSchool/', views.checkPersonalNumberAndGetTransferSchool, name="checkPersonalNo"),
    
    
    # Prmotions urls
    path('promotion/add/', views.PromotionAddView.as_view(), name="promotionAdd"),
    path('promotion/list/', views.PromotionsListView.as_view(), name="promotionList"),
    path('promotion/undo/<int:pk>/', views.PromotionUndoView, name="promotionUndo"),
    path('promotion/search/', views.PromotionSearchView.as_view(), name="promotionSearch"),
    path('checkPersonalNumberAndGetPromotionPost/', views.checkPersonalNumberAndGetPromotionPost, name="checkPersonalNoForPost"),
    
]
