from django.shortcuts import render
from .models import Case
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.safestring import mark_safe

# Create your views here.
def cases(request):
    cases_qs = Case.objects.all()
    row_data = [
        {
            'id': case.id,
            'description': case.description,
            'status': case.status,
            'category': case.category,
            'created_at': case.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        }
        for case in cases_qs
    ]

    context = {
        'title': 'Cases',
        'cases': cases_qs,
        'rowData': mark_safe(json.dumps(row_data)),
        'cases_count': cases_qs.count(),
    }

    return render(request, 'process/cases.html', context)

def case_detail(request, case_id):
    case = Case.objects.get(id=case_id)
    context = {
        'title': 'Case Detail',
        'case': case,
    }
    return render(request, 'process/case_detail.html', context)

def case_new(request):
    if request.method == 'POST':
        description = request.POST.get('description')
        status = request.POST.get('status')
        category = request.POST.get('category')
        case = Case.objects.create(
            description=description,
            status=status,
            category=category
        )
        return JsonResponse({'id': case.id, 'description': case.description, 'status': case.status, 'category': case.category})
    else:
        return render(request, 'process/case_new.html')
