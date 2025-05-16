from django import forms
from .models import Case, CustomerComplaint, Return, Credit

class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ['description', 'status', 'category', 'is_complaint', 'is_return', 'is_credit']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'status': forms.Select(),
            'category': forms.TextInput(attrs={'placeholder': 'Enter category'}),
        }
        labels = {
            'description': 'Case Description',
            'status': 'Status',
            'category': 'Category',
        }

class CustomerComplaintForm(forms.ModelForm):
    class Meta:
        model = CustomerComplaint
        fields = ['case','number', 'issue', 'resolution']
        widgets = {
            'issue': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'resolution': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }
        labels = {
            'case': 'Related Case',
            'issue': 'Issue Description',
            'resolution': 'Resolution Description',
        }

class ReturnForm(forms.ModelForm):
    class Meta:
        model = Return
        fields = ['case','number','authorized', 'reason', 'item_condition']
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'item_condition': forms.TextInput(attrs={'placeholder': 'Enter item condition'}),
        }
        labels = {
            'case': 'Related Case',
            'reason': 'Return Reason',
            'item_condition': 'Item Condition',
        }

class CreditForm(forms.ModelForm):
    class Meta:
        model = Credit
        fields = ['case', 'number','amount', 'credit_reason']
        widgets = {
            'amount': forms.NumberInput(attrs={'placeholder': 'Enter amount'}),
            'credit_reason': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }
        labels = {
            'case': 'Related Case',
            'amount': 'Credit Amount',
            'credit_reason': 'Credit Reason',
        }






    


