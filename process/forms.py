from django import forms
from .models import Case, CustomerComplaint, Return, Credit, Category, Scrap, File, Item
from .models import Category
from django.contrib.auth.models import User

class CaseForm(forms.ModelForm):

    class Meta:
        model = Case
        fields = ['customer_number','customer_name','title',  'is_complaint', 'is_return', 'is_credit', 'is_scrap']
        widgets = {
            'customer_number': forms.TextInput(attrs={'placeholder': 'Enter customer number'}),
            'customer_name': forms.TextInput(attrs={'placeholder': 'Enter customer name'}),
            'title': forms.TextInput(attrs={'placeholder': 'Enter case title'}),
        }
        widgets = {
            'status': forms.Select(),
        }
        labels = {
            'is_complaint': 'Complaint',
            'is_return': 'Return',
            'is_credit': 'Credit',
            'is_scrap': 'Scrap',
        }

class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['file']
        labels = {
            'file': 'Upload Files',
        }

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['cases','received_at','sku', 'description','qty', 'lot', 'wli_item', 'inspected', 'inspection_notes','inspection_initials','inspection_date']
        widgets = {
            'received_at': forms.DateInput(attrs={'type': 'date'}),
            'sku': forms.TextInput(attrs={'placeholder': 'Enter SKU'}),
            'description': forms.TextInput(attrs={'placeholder': 'Enter item description'}),
            'qty': forms.NumberInput(attrs={'placeholder': 'Enter quantity'}),
            'lot': forms.TextInput(attrs={'placeholder': 'Enter lot number'}),
            'wli_item': forms.CheckboxInput(attrs={'placeholder': 'Is this a WLI item?'}),
            'inspected': forms.CheckboxInput(),
            'inspection_notes': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'inspection_initials': forms.TextInput(attrs={'placeholder': 'Enter initials'}),
            'inspection_date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'wli_item': 'Check if this a WLI item. (If checked, the item has to be inspected by quality)',
            'inspected': 'Check if inspected',
        }

class CustomerComplaintForm(forms.ModelForm):
    class Meta:
        model = CustomerComplaint
        exclude = [
            'created_at',
            'created_by',
            'open_at',
            'closed_at',
            'request_submitted_at',
            'path_assigned_at',
            'investigation_in_progress_at',
            'disposition_at',
            'resolution_at',
        ]
        widgets = {
            'issue': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'disposition': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'resolution': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'reported_on': forms.DateInput(attrs={'type': 'date'}),
            'event_date': forms.DateInput(attrs={'type': 'date'}),
            'death_date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'case': 'Related Case',
            'issue': 'Issue Description',
            'resolution': 'Resolution Description',
            'departments': 'Departments to investigate (use Ctrl + Click to select multiple)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['received_by'].queryset = User.objects.filter(profile__active=True).order_by('first_name', 'last_name')



class ReturnForm(forms.ModelForm):
    class Meta:
        model = Return
        fields = [
            'case',
            'number',
            'authorized',
            'reason',
            'item_condition',
            'file',
            'fees',
            'charges',
            'taxes',
            'call_tags',
            'est_cost',
            'carrier_claim_number',
            'carrier_tracking_number',
            'replacement_invoice_number',
            'replacement_shipped',
            'payment_method_requested',
            'requested_credit_amount',
        ]
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'item_condition': forms.TextInput(attrs={'placeholder': 'Enter item condition'}),
            'file': forms.ClearableFileInput(),
            'est_cost': forms.NumberInput(attrs={'placeholder': 'Estimated cost'}),
            'carrier_claim_number': forms.TextInput(attrs={'placeholder': 'Carrier claim number'}),
            'carrier_tracking_number': forms.TextInput(attrs={'placeholder': 'Carrier tracking number'}),
            'replacement_invoice_number': forms.TextInput(attrs={'placeholder': 'Replacement invoice number'}),
            'requested_credit_amount': forms.NumberInput(attrs={'placeholder': 'Requested credit amount'}),
        }
        labels = {
            'case': 'Related Case',
            'reason': 'Return Reason',
            'item_condition': 'Item Condition',
            'file': 'Attachment',
            'fees': '20% Restocking Fee Applies',
            'charges': 'Shipping charges will added',
            'taxes': 'Credit/Return is taxable',
            'call_tags': 'Call Tags',
            'est_cost': 'Estimated Cost',
            'carrier_claim_number': 'Carrier Claim Number',
            'carrier_tracking_number': 'Carrier Tracking Number',
            # 'replacement_invoice_number': 'Replacement Invoice Number',  # Removed as requested
            'replacement_shipped': 'Replacement Shipped',
            'payment_method_requested': 'Payment Method Requested',
            'requested_credit_amount': 'Requested Credit Amount',
        }

class CreditForm(forms.ModelForm):
    class Meta:
        model = Credit
        fields = ['case', 'number','status','amount', 'credit_reason']
        widgets = {
            'amount': forms.NumberInput(attrs={'placeholder': 'Enter amount'}),
            'credit_reason': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }
        labels = {
            'case': 'Related Case',
            'amount': 'Credit Amount',
            'credit_reason': 'Credit Reason',
        }

class ScrapForm(forms.ModelForm):
    class Meta:
        model = Scrap
        fields = ['case', 'number','status','reason']
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }
        labels = {
            'case': 'Related Case',
            'reason': 'Scrap Reason',
        }






    


