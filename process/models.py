from django.db import models
from django.contrib.auth.models import User
from users.models import Department
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.images import get_image_dimensions
from django.core.exceptions import ValidationError
from PIL import Image
import io

class Item(models.Model):
    sku = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True, null=True)
    qty = models.IntegerField(default=0)
    lot = models.CharField(max_length=100, blank=True, null=True)
    wli_item = models.BooleanField(default=False)
    inspected = models.BooleanField(default=False)
    inspection_notes = models.TextField(blank=True, null=True)
    inspection_date = models.DateTimeField(blank=True, null=True)
    inspection_initials = models.CharField(max_length=10, blank=True, null=True)
    received_at = models.DateField(blank=True, null=True)
    cases = models.ForeignKey('Case', on_delete=models.CASCADE, related_name='items', blank=True, null=True)
    complaint = models.ForeignKey('CustomerComplaint', on_delete=models.CASCADE, related_name='items', blank=True, null=True)
    returns = models.ForeignKey('Return', on_delete=models.CASCADE, related_name='items', blank=True, null=True)
    credit = models.ForeignKey('Credit', on_delete=models.CASCADE, related_name='items', blank=True, null=True)
    scrap = models.ForeignKey('Scrap', on_delete=models.CASCADE, related_name='items', blank=True, null=True)
    created_at = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.sku
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
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_cases', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_complaint = models.BooleanField(default=True)
    is_return = models.BooleanField(default=True)
    is_credit = models.BooleanField(default=True)
    is_scrap = models.BooleanField(default=True)


    def __str__(self):
        return f"Case #{self.id}"

    def clean(self):
        super().clean()
        if not self.is_complaint and not self.is_return and not self.is_credit and not self.is_scrap:
            raise ValidationError("At least one of the complaint, return, credit, or scrap must be selected.")

        # resize image to low quality
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

class Category(models.Model):
    code = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title

class CustomerComplaint(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='complaints')
    reported_on = models.DateField(default=timezone.now, blank=True, null=True)
    received_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_complaints', blank=True, null=True)
    event_date = models.DateField(blank=True, null=True)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_complaints', blank=True, null=True)
    STATUS_COMPLAINT_CHOICES = [
        ('open', 'Open'),
        ('request_submitted', 'Request Submitted'),
        ('path_assigned', 'Path Assigned'),
        ('investigation_in_progress', 'Investigation In Progress'),
        ('disposition', 'Disposition'),
        ('resolution', 'Resolution'),
        ('closed', 'Closed'),
    ]
    status = models.CharField(max_length=100, choices=STATUS_COMPLAINT_CHOICES, default='open')
    classification = models.CharField(max_length=100, choices=[
        ('shipping', 'Shipping'),
        ('contamination', 'Contamination'),
        ('irritation', 'Irritation'),
        ('leaking', 'Leaking'),
        ('package_issue', 'Package Issue'),
        ('efficacy', 'Efficacy'),
        ('expired', 'Expired'),
        ('cloudy', 'Cloudy'),
        ('other', 'Other'),
    ], default='other', blank=True, null=True)
    number = models.CharField(max_length=100, blank=True, null=True)
    # time stamp quality received
    request_submitted_at = models.DateTimeField(blank=True, null=True)
    path_assigned_at = models.DateTimeField(blank=True, null=True)
    investigation_in_progress_at = models.DateTimeField(blank=True, null=True)
    disposition_at = models.DateTimeField(blank=True, null=True)
    resolution_at = models.DateTimeField(blank=True, null=True)
    closed_at = models.DateTimeField(blank=True, null=True)
    disposition = models.TextField(blank=True, null=True)
    resolution = models.TextField(blank=True, null=True)
    departments = models.ManyToManyField(Department, related_name='complaints', blank=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    enduser_name = models.CharField(max_length=200, blank=True, null=True)
    enduser_email = models.EmailField(blank=True, null=True)
    enduser_phone = models.CharField(max_length=20, blank=True, null=True)
    enduser_address = models.CharField(max_length=255, blank=True, null=True)
    death = models.BooleanField(default=False)
    death_date = models.DateField(blank=True, null=True)
    life_threatening = models.BooleanField(default=False)
    hospitalization = models.BooleanField(default=False)
    issue = models.TextField()
    path = models.CharField(max_length=100, choices=[
        ('path1', 'Path 1: 29, 33 – Customer Resolution (Customer Service or Sales); 24 – FDA Report Assessment (QA); 26, 27 – Trend Check (QA);25, 28, 30 to 32 – QA Investigation'),
        ('path2', 'Path 2: 29, 33 – Customer Resolution (Customer Service or Sales); 26-27 – Trend Check (QA); 25, 28, 30 to 32 – QA Investigation.'),
        ('path3', 'Path 3: 29, 33 – Customer Resolution (customer service or sales); 26, 27 – Trend Verification (QA); Notify Vendor (Purchasing)'),
        ('path4', 'Path 4: 29, 33 – Customer Resolution (Customer Service or Sales); 26, 27 – Trend Verification (QA); 28 and 31, 32 – Incident Investigation (Customer Service or Sales/Shipping)'),
        ('path5', 'Path 5: 29, 33 – Customer Resolution (Customer Service or Sales); 24 – FDA Report Evaluation (QA); 26, 27 – Trend Check (QA), Notify Vendor (QA or Purchases).'),
    ], blank=True, null=True)
    image = models.ImageField(upload_to='complaint/', blank=True, null=True)


class Return(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='returns')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_returns', blank=True, null=True)
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
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_credits', blank=True, null=True)
    STATUS_CREDIT_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
    ]
    status = models.CharField(max_length=100, choices=STATUS_CREDIT_CHOICES, default='open')
    number = models.CharField(max_length=100, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    credit_reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Scrap(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='scraps')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_scraps', blank=True, null=True)
    STATUS_SCRAP_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
    ]
    status = models.CharField(max_length=100, choices=STATUS_SCRAP_CHOICES, default='open')
    number = models.CharField(max_length=100, blank=True, null=True)
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class File(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='case_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_files', blank=True, null=True)

    def __str__(self):
        return f"File for Case #{self.case.id} - {self.file.name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        image = getattr(self, 'file')
        if image and hasattr(image, 'path'):
            try:
                img = Image.open(image.path)
                if img.format in ['JPEG', 'PNG', 'GIF', 'BMP']:
                    if img.height > 500 or img.width > 500:
                        output_size = (500, 500)
                        img.thumbnail(output_size)
                        img.save(image.path)
            except Exception:
                pass