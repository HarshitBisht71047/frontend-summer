from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_pdf, name='upload_pdf'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('symptom_input/', views.symptom_input, name='symptom_input'),

]
