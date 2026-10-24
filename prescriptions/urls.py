

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add/', views.add_prescription, name='add_prescription'),
    path('edit/<int:pk>/', views.edit_prescription, name='edit_prescription'),
    path('delete/<int:pk>/', views.delete_prescription, name='delete_prescription'), 
    path('patient-history/<str:patient_name>/', views.patient_history, name='patient_history'), 
    path('export/', views.export_prescriptions, name='export_prescriptions'),

]
