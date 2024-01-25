from django.urls import path
from django.views.generic import TemplateView
app_name="reports"
from . import views
urlpatterns = [
    path('proforma/<int:pk>',views.MonthlyReturnProFormaView.as_view(), name="ReturnProforma"),
    path('proforma/download/<int:pk>',views.DownloadMonthlyReturnProForma.as_view(), name="DownloadReturnProforma"),
    
    path('template/',views.Report_Tempalte.as_view(), name="reportTemplate"),
    
    # School Reports
    path('school/all/', views.School_List_Report.as_view(), name="schoolAll"),
    
    # Teacher Reports
    path('govt-election/teachers/list/', views.list_of_teachers_for_govt_election, name="govtElectionList"),
    path('teachers/list/', views.list_of_teachers_Report, name="teacherReport"),
    path('c/', TemplateView.as_view(template_name="reports/teachers/custome.html")),


    # SEPARATE REPORTS
    
    path("get/teachers/report/<int:pk>", views.showTeacherReport, name="getTeacherReport"),
    path("get/staff/report/<int:pk>", views.showStaffReport, name="getStaffReport"),
    path("get/ptcInformation/report/<int:pk>", views.showPtcInformationReport, name="getPtcInformationReport"),
    path("get/building/report/<int:pk>", views.showBuildingReport, name="getBuildingReport"),
    path("get/student/strength/report/<int:pk>", views.showStudentStrengthReport, name="getStudentStrengthReport"),
    path("get/stock/report/<int:pk>", views.showStockReport, name="getStockReport"),

]
