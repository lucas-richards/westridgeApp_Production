from django.shortcuts import render
from .models import Case, CustomerComplaint, Return, Credit, Scrap
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.safestring import mark_safe
from .forms import CaseForm, CustomerComplaintForm, ReturnForm, CreditForm, ScrapForm, FileForm, ItemForm
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import redirect
from django import forms
from django.urls import reverse
from django.utils import timezone
from pytz import timezone as pytz_timezone

# Create your views here.
def dashboard(request):
    cases_qs = Case.objects.all().order_by('-id')
    open_cases_count = cases_qs.filter(status='open').count()
    closed_cases_count = cases_qs.filter(status='closed').count()
    complaints_qs = CustomerComplaint.objects.all()
    open_complaints = complaints_qs.filter(status='open').count()
    total_complaints = complaints_qs.count()
    returns_qs = Return.objects.all()
    open_returns = returns_qs.filter(status='open').count()
    total_returns = returns_qs.count()
    credits_qs = Credit.objects.all()
    open_credits = credits_qs.filter(status='open').count()
    total_credits = credits_qs.count()
    scraps_qs = Scrap.objects.all()
    open_scraps = scraps_qs.filter(status='open').count()
    total_scraps = scraps_qs.count()
    
    context = {
        'title': 'Dashboard',
        'cases': cases_qs,
        'open_cases_count': open_cases_count,
        'closed_cases_count': closed_cases_count,
        'total_complaints': total_complaints,
        'open_complaints': open_complaints,
        'total_returns': total_returns,
        'open_returns': open_returns,
        'total_credits': total_credits,
        'open_credits': open_credits,
        'total_scraps': total_scraps,
        'open_scraps': open_scraps,
    }
    
    return render(request, 'process/dashboard.html', context)

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
    if request.method == 'POST':
        fileform = FileForm(request.POST, request.FILES)
        if fileform.is_valid():
            file_instance = fileform.save(commit=False)
            file_instance.case = case
            file_instance.save()
            messages.success(request, 'File uploaded successfully!')
            return redirect('process-case-detail', case_id=case.id)
        else:
            messages.error(request, 'Error uploading file. Please check the form.')
    else:
        fileform = FileForm()

    files = case.files.exclude(file__iregex=r'\.(jpg|jpeg|png|gif|bmp|webp)$')
    images = case.files.filter(file__iregex=r'\.(jpg|jpeg|png|gif|bmp|webp)$')
    print(images)

    context = {
        'title': 'Case Detail',
        'case': case,
        'fileform': fileform,
        'files': files,
        'images': images,
        'complaints': case.complaints.all(),
        'returns': case.returns.all(),
        'credits': case.credits.all(),
        'scraps': case.scraps.all(),
    }
    return render(request, 'process/case_detail.html', context)

def case_update_status(request, case_id):
    case = Case.objects.get(id=case_id)
    if case.status.lower() == 'open':
        case.status = 'closed'
    else:
        case.status = 'open'
    print(case.status)
    case.save()
    messages.success(request, 'Case status updated successfully!')
    return redirect('process-case-detail', case_id=case.id)

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
        form = CaseForm(request.POST, request.FILES)
        
        if form.is_valid():
            case = form.save(commit=False)
            case.created_by = request.user
            case.save()
            messages.success(request, 'Case created successfully!')
            return redirect('process-case-detail', case_id=case.id)
    else:
        form = CaseForm()
    return render(request, 'process/case_new.html', {'form': form})

def customer_complaint_new(request, case_id):
    case = Case.objects.get(id=case_id)
    if request.method == 'POST':
        form = CustomerComplaintForm(request.POST)
        print(form.errors)
        if form.is_valid():
            customer_complaint = form.save(commit=False)
            customer_complaint.created_by = request.user
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
        status_to_field = {
            'request_submitted': 'request_submitted_at',
            'path_assigned': 'path_assigned_at',
            'investigation_in_progress': 'investigation_in_progress_at',
            'disposition': 'disposition_at',
            'resolution': 'resolution_at',
            'closed': 'closed_at',
        }
        status = form['status'].value()

        

        complaint.status = status
        print(form.errors)
        if form.is_valid():
            if 'save_and_next' in request.POST:
                current_status = form.cleaned_data['status']
                
                # Define status progression
                status_flow = [
                    'open',
                    'request_submitted',
                    'path_assigned',
                    'investigation_in_progress',
                    'disposition',
                    'resolution',
                    'closed'
                ]

                try:
                    next_index = status_flow.index(current_status) + 1
                    if next_index < len(status_flow):
                        form.instance.status = status_flow[next_index]
                        if status_flow[next_index] in status_to_field:
                            setattr(complaint, status_to_field[status_flow[next_index]], timezone.now())
                except ValueError:
                    pass  # Handle unexpected status gracefully

            form.save()
            messages.success(request, 'Customer complaint updated successfully!')
        else:
            messages.error(request, f'Error updating customer complaint. Please check the form.{form.errors}')
        return redirect('process-case-detail', case_id=case.id)
            
    else:
        form = CustomerComplaintForm(instance=complaint)
        form.fields['case'].widget = forms.HiddenInput()

    
    pacific = pytz_timezone('US/Pacific')

    def to_pacific(dt):
        if dt:
            if timezone.is_naive(dt):
                dt = timezone.make_aware(dt)
            return dt.astimezone(pacific).strftime('%Y-%m-%d %H:%M:%S')
        return ""

    steps = [
        {"label": "Open", "date": to_pacific(complaint.created_at)},
        {"label": "Request Submitted", "date": to_pacific(complaint.request_submitted_at)},
        {"label": "Path Assigned", "date": to_pacific(complaint.path_assigned_at)},
        {"label": "Investigation In Progress", "date": to_pacific(complaint.investigation_in_progress_at)},
        {"label": "Disposition", "date": to_pacific(complaint.disposition_at)},
        {"label": "Resolution", "date": to_pacific(complaint.resolution_at)},
        {"label": "Closed", "date": to_pacific(complaint.closed_at)}
    ]

    current_step = complaint.get_status_display() if complaint.status else 'Open'

    context = {
        'form': form,
        'case': case,
        'complaint': complaint,
        'steps': steps,
        'current_step': current_step,
        'wrapper_class': 'progress-bar-wrapper'
    }

    return render(request, 'process/customer_complaint_new.html', context)

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

    steps = [
        {"label": "Open", "date": return_instance.created_at.strftime('%Y-%m-%d %H:%M:%S')},
        {"label": "Request Submitted", "date": "2025-05-02 10:30:00"},
        {"label": "Path Assigned", "date": "2025-05-03 14:15:00"},
        {"label": "Investigation In Progress", "date": "2025-05-05 11:45:00"},
        {"label": "Resolution", "date": "2025-05-08 16:20:00"},
        {"label": "Closed", "date": "2025-05-10 17:00:00"}
    ]

    current_step = return_instance.get_status_display() if return_instance.status else 'Open'

    context = {
        'form': form,
        'case': case,
        'return_instance': return_instance,
        'steps': steps,
        'current_step': current_step,
        'wrapper_class': 'progress-bar-wrapper'
    }
    return render(request, 'process/return_new.html', context)

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

def item_new(request, case_id):
    case = Case.objects.get(id=case_id)
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.cases = case
            item.save()
            messages.success(request, 'Item created successfully!')
            return redirect('process-case-detail', case_id=case.id)
    else:
        form = ItemForm()
        form.fields['cases'].initial = case.id
        form.fields['cases'].widget = forms.HiddenInput()
    return render(request, 'process/item_new.html', {'form': form, 'case': case})

def item_edit(request, case_id, item_id):
    case = Case.objects.get(id=case_id)
    item = case.items.get(id=item_id)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item updated successfully!')
            return redirect('process-case-detail', case_id=case.id)
    else:
        form = ItemForm(instance=item)
        form.fields['cases'].widget = forms.HiddenInput()
    return render(request, 'process/item_new.html', {'form': form, 'case': case, 'item': item})

def item_delete(request, case_id, item_id):
    case = Case.objects.get(id=case_id)
    item = case.items.get(id=item_id)
    item.delete()
    messages.success(request, 'Item deleted successfully!')
    return redirect('process-case-detail', case_id=case.id)