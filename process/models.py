from django.db import models

# Create your models here.
class Case(models.Model):
    customer_number = models.CharField(max_length=100, blank=True)
    customer_name = models.CharField(max_length=200, blank=True)
    title = models.CharField(max_length=200, blank=True)
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
    ]
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    is_complaint = models.BooleanField(default=True)
    is_return = models.BooleanField(default=True)
    is_credit = models.BooleanField(default=True)
    is_scrap = models.BooleanField(default=True)

    def __str__(self):
        return f"Case #{self.id}"

class Category(models.Model):
    code = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title

class CustomerComplaint(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='complaints')
    STATUS_COMPLAINT_CHOICES = [
        ('open', 'Open'),
        ('quality', 'Quality'),
        ('customer_service', 'Customer Service'),
        ('sales', 'Sales'),
        ('warehouse', 'Warehouse'),
        ('production', 'Production'),
        ('closed', 'Closed'),
    ]
    status = models.CharField(max_length=100, choices=STATUS_COMPLAINT_CHOICES, default='open')
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True, related_name='cases')
    number = models.CharField(max_length=100, blank=True, null=True)
    issue = models.TextField()
    resolution = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Return(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='returns')
    STATUS_RETURN_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
    ]
    status = models.CharField(max_length=100, choices=STATUS_RETURN_CHOICES, default='open')
    number = models.CharField(max_length=100, blank=True, null=True)
    authorized = models.BooleanField(default=False)
    reason = models.TextField()
    file = models.FileField(upload_to='returns/', blank=True, null=True)
    fees = models.BooleanField(default=False)
    charges = models.BooleanField(default=False)
    taxes = models.BooleanField(default=False)
    # number int
    call_tags = models.IntegerField(default=0)
    est_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    carrier_claim_number = models.CharField(max_length=100, blank=True, null=True)
    carrier_tracking_number = models.CharField(max_length=100, blank=True, null=True)
    replacement_invoice_number = models.CharField(max_length=100, blank=True, null=True)
    replacement_shipped = models.BooleanField(default=False)
    PAYMENT = [
        ('Credit', 'Credit'),
        ('Credit Card', 'Credit Card'),
    ]
    payment_method_requested = models.CharField(max_length=100, choices=PAYMENT, default='open')
    requested_credit_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    item_condition = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

class Credit(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='credits')
    STATUS_CREDIT_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
    ]
    status = models.CharField(max_length=100, choices=STATUS_CREDIT_CHOICES, default='open')
    number = models.CharField(max_length=100, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    credit_reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)