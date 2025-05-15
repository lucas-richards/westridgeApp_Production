from django.urls import path
from . import views

urlpatterns = [
    path('', views.cases, name='process-cases'),
    path('cases/<int:case_id>/', views.case_detail, name='process-case-detail'),
    path('cases/new/', views.case_detail, name='process-case-new'),

]
