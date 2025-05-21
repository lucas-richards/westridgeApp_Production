from django import forms
from .models import Case, CustomerComplaint, Return, Credit, Category, Scrap
from .models import Category

class CaseForm(forms.ModelForm):

    class Meta:
        model = Case
        fields = ['customer_number','customer_name','title',  'is_complaint', 'is_return', 'is_credit', 'is_scrap']
        widgets = {
            'status': forms.Select(),
        }
        labels = {
            'is_complaint': 'Complaint',
            'is_return': 'Return',
            'is_credit': 'Credit',
            'is_scrap': 'Scrap',
        }

class CustomerComplaintForm(forms.ModelForm):
    class Meta:
        model = CustomerComplaint
        fields = ['case','number','status', 'issue', 'resolution']
        widgets = {
            'number': forms.TextInput(attrs={'placeholder': 'This number is provided by quality once it is submitted'}),
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






    


