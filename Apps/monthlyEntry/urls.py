from django.urls import path
from . import views
app_name = "entry"
urlpatterns = [
    # Builiding paths
    path('building/add/', views.SchoolBuildingMonthlyEntryView.as_view(), name="buildingAdd"),
    path('building/detail/<int:pk>/', views.SchoolBuildingView.as_view(), name="buildingDetail"),
    path('building/delete/<int:pk>/', views.delete_building, name="buildingDelete"),
    path('building/fill/', views.buildingRecord_fill_from_prev, name="buildingfill"),
    
    # Teacher Monthly paths
    path('teacher/add/', views.TeacherMonthlyEntryView.as_view(), name="teacherMonthlyAdd"),
    path('teacher/list/<int:id>/', views.TeacherMonthlyEntryListView.as_view(), name="teacherMonthlyList"),
    path('teacher/delete/<int:pk>/', views.delete_TeacherMonthlyEntry, name="teacherMonthlyDelete"),
    
    # Students Strength Paths
    path('student-strength/add/', views.StudentStrengthMonthlyEntryView.as_view(), name="studentStrengthAdd"),
    path('student-strength/detail/<int:pk>/', views.StudentStrengthDetailView.as_view(), name="studentStrengthDetail"),
    path('student-strength/delete/<int:pk>/', views.delete_StudentStrength, name="studentStrengthDelete"),
    path('student-strength/add/prev/', views.StudentStrengthSavePrev.as_view(), name="StudentStrengthSavePrev"),
    
    # Stock paths
    path('stock/add/', views.SchoolStockMonthlyEntryView.as_view(), name="schoolStockAdd"),
    path('stock/detail/<int:pk>/', views.StockDetailView.as_view(), name="schoolStockDetail"),
    path('stock/delete/<int:pk>/', views.delete_Stock, name="schoolStockDetelet"),
    path('stock/add/prev/', views.SchoolStockMonthlyEntrySavePrev.as_view(), name="SchoolStockMonthlyEntrySavePrev"),
    
    # Staff Avilibility
    path('staff-avalibility/add/', views.StaffAvalibilityMonthlyEntryView.as_view(), name="staffAvalibilityAdd"),
    path('get-filled/staff/', views.get_filled_staff, name="getFilledStaff"),
    path('staff/detail/<int:pk>/', views.StaffAvalibilityDetailView.as_view(), name="staffDetail"),
    path('staff/delete/<int:pk>/', views.delete_staff,name="staffDelete"),
    path('staff/add/prev/', views.StaffAvalibilitySavePrev.as_view(),name="staffAvalibilityAddPrev"),
   
    # PTC INFORMATION
    path('ptc-information/add/', views.PTC_INFORMATIONEntryView.as_view(), name="ptcInformationAdd"),
    path('ptc-information/detail/<int:pk>', views.PTC_INFOLISTView.as_view(), name="ptcInformationDetail"),
    # path('staff/detail/<int:pk>/', views.StaffAvalibilityDetailView.as_view(), name="staffDetail"),
  path('ptc-information/delete/<int:pk>/', views.delete_ptcInfo, name="ptcInformationDelete"),
  path('ptc-information/fill/prev/', views.ptcRecord_fill_from_prev, name="ptcRecord_fill_from_prev"),
    
    path('setting/', views.SettingForMonthlyEntryView.as_view(), name="setting"),
    path("filter/", views.get_filter_template.as_view(), name="getFilterTemplate"),
    
    
    path('show/record/', views.ShowRecordsView.as_view(), name="showRecords"),
    path('show/records/', views.showRecordFromSession, name="showRecordsFromSession"),
    path('show/record/<int:id>/', views.ShowRecordsView.as_view(), name="showSingleRecord"),
    path('record/delete/<int:pk>/', views.delete_record, name="deleterecord"),
    path('record/delete/client/<int:pk>/', views.delete_record_from_clientSide, name="deleteRecordFromClient")
    

    
]
