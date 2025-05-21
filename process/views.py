from django.shortcuts import render
from .models import Case
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.safestring import mark_safe
from .forms import CaseForm, CustomerComplaintForm, ReturnForm, CreditForm, ScrapForm
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import redirect
from django import forms
from django.urls import reverse

# Create your views here.
def cases(request):
    cases_qs = Case.objects.all().order_by('-id')
    open_cases_count = cases_qs.filter(status='open').count()
    
    row_data = [
        {
            'id': case.id,
            'title': case.title,
            'status': case.status,
            'created_at': case.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'is_complaint': case.is_complaint,
            'is_return': case.is_return,
            'is_credit': case.is_credit,
            'is_scrap': case.is_scrap,
            'complaint_number': case.complaints.first().number if case.complaints.exists() and case.complaints.first().number else None,
            'return_number': case.returns.first().number if case.returns.exists() and case.returns.first().number else None,
            'credit_number': case.credits.first().number if case.credits.exists() and case.credits.first().number else None,
            'scrap_number': case.scraps.first().number if case.scraps.exists() and case.scraps.first().number else None,
        }
        for case in cases_qs
    ]

    context = {
        'title': 'Cases',
        'cases': cases_qs,
        'rowData': mark_safe(json.dumps(row_data)),
        'cases_count': open_cases_count,
    }

    return render(request, 'process/cases.html', context)

def case_detail(request, case_id):
    case = Case.objects.get(id=case_id)
    complaints = case.complaints.all()
    returns = case.returns.all()
    credit = case.credits.all()
    context = {
        'title': 'Case Detail',
        'case': case,
        'complaints': complaints,
        'returns': returns,
        'credits': credit,
    }
    return render(request, 'process/case_detail.html', context)

def case_edit(request, case_id):
    case = Case.objects.get(id=case_id)
    if request.method == 'POST':
        form = CaseForm(request.POST, instance=case)
        if form.is_valid():
            form.save()
            messages.success(request, 'Case updated successfully!')
            return redirect('process-case-detail', case_id=case.id)
    else:
        form = CaseForm(instance=case)
    return render(request, 'process/case_new.html', {'form': form, 'case': case})

def case_delete(request, case_id):
    case = Case.objects.get(id=case_id)
    case.delete()
    messages.success(request, 'Case deleted successfully!')
    return redirect('process-cases')

def case_new(request):
    if request.method == 'POST':
        form = CaseForm(request.POST)
        if form.is_valid():
            case = form.save()
            messages.success(request, 'Case created successfully!')
            return redirect('process-case-detail', case_id=case.id)
    else:
        form = CaseForm()
    return render(request, 'process/case_new.html', {'form': form})

def customer_complaint_new(request, case_id):
    case = Case.objects.get(id=case_id)
    if request.method == 'POST':
        form = CustomerComplaintForm(request.POST)
        if form.is_valid():
            customer_complaint = form.save(commit=False)
            customer_complaint.case = case
            customer_complaint.save()
            messages.success(request, 'Customer complaint created successfully!')
            return redirect('process-case-detail', case_id=case.id)
    else:
        form = CustomerComplaintForm()
        form.fields['case'].initial = case.id
        form.fields['case'].widget = forms.HiddenInput()
    return render(request, 'process/customer_complaint_new.html', {'form': form, 'case': case})

def customer_complaint_edit(request, case_id, complaint_id):
    case = Case.objects.get(id=case_id)
    complaint = case.complaints.get(id=complaint_id)
    if request.method == 'POST':
        form = CustomerComplaintForm(request.POST, instance=complaint)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer complaint updated successfully!')
            return redirect('process-case-detail', case_id=case.id)
    else:
        form = CustomerComplaintForm(instance=complaint)
        form.fields['case'].widget = forms.HiddenInput()
    return render(request, 'process/customer_complaint_new.html', {'form': form, 'case': case, 'complaint': complaint})

def customer_complaint_delete(request, case_id, complaint_id):
    case = Case.objects.get(id=case_id)
    complaint = case.complaints.get(id=complaint_id)
    complaint.delete()
    messages.success(request, 'Customer complaint deleted successfully!')
    return redirect('process-case-detail', case_id=case.id)

def return_new(request, case_id):
    case = Case.objects.get(id=case_id)
    if request.method == 'POST':
        form = ReturnForm(request.POST)
        if form.is_valid():
            return_instance = form.save(commit=False)
            return_instance.case = case
            return_instance.save()
            messages.success(request, 'Return created successfully!')
            return redirect('process-case-detail', case_id=case.id)
    else:
        form = ReturnForm()
        form.fields['case'].initial = case.id
        form.fields['case'].widget = forms.HiddenInput()
    return render(request, 'process/return_new.html', {'form': form, 'case': case})

def return_edit(request, case_id, return_id):
    case = Case.objects.get(id=case_id)
    return_instance = case.returns.get(id=return_id)
    if request.method == 'POST':
        form = ReturnForm(request.POST, instance=return_instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Return updated successfully!')
            return redirect('process-case-detail', case_id=case.id)
    else:
        form = ReturnForm(instance=return_instance)
        form.fields['case'].widget = forms.HiddenInput()
    return render(request, 'process/return_new.html', {'form': form, 'case': case, 'return_instance': return_instance})

def return_delete(request, case_id, return_id):
    case = Case.objects.get(id=case_id)
    return_instance = case.returns.get(id=return_id)
    return_instance.delete()
    messages.success(request, 'Return deleted successfully!')
    return redirect('process-case-detail', case_id=case.id)

def credit_new(request, case_id):
    case = Case.objects.get(id=case_id)
    if request.method == 'POST':
        form = CreditForm(request.POST)
        if form.is_valid():
            credit = form.save(commit=False)
            credit.case = case
            credit.save()
            messages.success(request, 'Credit created successfully!')
            return redirect('process-case-detail', case_id=case.id)
    else:
        form = CreditForm()
        form.fields['case'].initial = case.id
        form.fields['case'].widget = forms.HiddenInput()
    return render(request, 'process/credit_new.html', {'form': form, 'case': case})

def credit_edit(request, case_id, credit_id):
    case = Case.objects.get(id=case_id)
    credit = case.credits.get(id=credit_id)
    if request.method == 'POST':
        form = CreditForm(request.POST, instance=credit)
        if form.is_valid():
            form.save()
            messages.success(request, 'Credit updated successfully!')
            return redirect('process-case-detail', case_id=case.id)
    else:
        form = CreditForm(instance=credit)
        form.fields['case'].widget = forms.HiddenInput()
    return render(request, 'process/credit_new.html', {'form': form, 'case': case, 'credit': credit})

def credit_delete(request, case_id, credit_id):
    case = Case.objects.get(id=case_id)
    credit = case.credits.get(id=credit_id)
    credit.delete()
    messages.success(request, 'Credit deleted successfully!')
    return redirect('process-case-detail', case_id=case.id)

def scrap_new(request, case_id):
    case = Case.objects.get(id=case_id)
    if request.method == 'POST':
        form = ScrapForm(request.POST)
        if form.is_valid():
            scrap = form.save(commit=False)
            scrap.case = case
            scrap.save()
            messages.success(request, 'Scrap created successfully!')
            return redirect('process-case-detail', case_id=case.id)
    else:
        form = ScrapForm()
        form.fields['case'].initial = case.id
        form.fields['case'].widget = forms.HiddenInput()
    return render(request, 'process/scrap_new.html', {'form': form, 'case': case})

def scrap_edit(request, case_id, scrap_id):
    case = Case.objects.get(id=case_id)
    scrap = case.scraps.get(id=scrap_id)
    if request.method == 'POST':
        form = ScrapForm(request.POST, instance=scrap)
        if form.is_valid():
            form.save()
            messages.success(request, 'Scrap updated successfully!')
            return redirect('process-case-detail', case_id=case.id)
    else:
        form = ScrapForm(instance=scrap)
        form.fields['case'].widget = forms.HiddenInput()
    return render(request, 'process/scrap_new.html', {'form': form, 'case': case, 'scrap': scrap})

def scrap_delete(request, case_id, scrap_id):
    case = Case.objects.get(id=case_id)
    scrap = case.scraps.get(id=scrap_id)
    scrap.delete()
    messages.success(request, 'Scrap deleted successfully!')
    return redirect('process-case-detail', case_id=case.id)
