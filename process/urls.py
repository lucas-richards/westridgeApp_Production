from django.urls import path
from . import views

urlpatterns = [
    path('', views.cases, name='process-cases'),
    path('cases/new/', views.case_new, name='process-case-new'),
    path('cases/edit/<int:case_id>/', views.case_edit, name='process-case-edit'),
    path('cases/<int:case_id>/', views.case_detail, name='process-case-detail'),
    path('cases/<int:case_id>/delete/', views.case_delete, name='process-case-delete'),
    # new customer complain for the case
    path('cases/<int:case_id>/customer-complaint/new/', views.customer_complaint_new, name='process-customer-complaint-new'),
    path('cases/<int:case_id>/customer-complaint/edit/<int:complaint_id>/', views.customer_complaint_edit, name='process-complaint-edit'),
    path('cases/<int:case_id>/customer-complaint/delete/<int:complaint_id>/', views.customer_complaint_delete, name='process-complaint-delete'),
    # new return for the case
    path('cases/<int:case_id>/return/new/', views.return_new, name='process-return-new'),
    path('cases/<int:case_id>/return/edit/<int:return_id>/', views.return_edit, name='process-return-edit'),
    path('cases/<int:case_id>/return/delete/<int:return_id>/', views.return_delete, name='process-return-delete'),
    # new credit for the case
    path('cases/<int:case_id>/credit/new/', views.credit_new, name='process-credit-new'),
    path('cases/<int:case_id>/credit/edit/<int:credit_id>/', views.credit_edit, name='process-credit-edit'),
    path('cases/<int:case_id>/credit/delete/<int:credit_id>/', views.credit_delete, name='process-credit-delete'),
    # new process scrap
    path('cases/<int:case_id>/scrap/new/', views.scrap_new, name='process-scrap-new'),
    path('cases/<int:case_id>/scrap/edit/<int:scrap_id>/', views.scrap_edit, name='process-scrap-edit'),
    path('cases/<int:case_id>/scrap/delete/<int:scrap_id>/', views.scrap_delete, name='process-scrap-delete'),

]
