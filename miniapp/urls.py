from django.urls import path,include
from . import views

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("employees/", views.employee_list, name="employee_list"),
    path("employees/<int:id>/", views.employee_detail, name="employee_detail"),
    path("employees/add/", views.employee_form, name="employee_form"),   
    path('employees/<int:id>/edit/', views.employee_update, name='employee_update'),
    path('employees/<int:id>/delete/', views.employee_delete, name='employee_delete'),
]