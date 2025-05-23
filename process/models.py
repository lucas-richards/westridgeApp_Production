from django.db import models
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.images import get_image_dimensions
from django.core.exceptions import ValidationError
from PIL import Image
import io


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
    # add three files or images
    image1 = models.ImageField(upload_to='cases/', blank=True, null=True)
    image2 = models.ImageField(upload_to='cases/', blank=True, null=True)
    image3 = models.ImageField(upload_to='cases/', blank=True, null=True)


    def __str__(self):
        return f"Case #{self.id}"

    def clean(self):
        super().clean()
        if not self.is_complaint and not self.is_return and not self.is_credit and not self.is_scrap:
            raise ValidationError("At least one of the complaint, return, credit, or scrap must be selected.")

        # resize image to low quality
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        for image_field in ['image1', 'image2', 'image3']:
            image = getattr(self, image_field)
            if image and hasattr(image, 'path'):
                try:
                    img = Image.open(image.path)
                    if img.height > 300 or img.width > 300:
                        output_size = (300, 300)
                        img.thumbnail(output_size)
                        img.save(image.path)
                except Exception:
                    pass

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
        ('request_submitted', 'Request Submitted'),
        ('path_assigned', 'Path Assigned'),
        ('investigation_in_progress', 'Investigation In Progress'),
        ('resolution', 'Resolution'),
        ('closed', 'Closed'),
    ]
    status = models.CharField(max_length=100, choices=STATUS_COMPLAINT_CHOICES, default='open')
    sku = models.CharField(max_length=100, blank=True, null=True)
    lot_number = models.CharField(max_length=100, blank=True, null=True)
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
    ], default='other')
    number = models.CharField(max_length=100, blank=True, null=True)
    # time stamp quality received
    request_submitted_at = models.DateTimeField(blank=True, null=True)
    path_assigned_at = models.DateTimeField(blank=True, null=True)
    investigation_in_progress_at = models.DateTimeField(blank=True, null=True)
    resolution_at = models.DateTimeField(blank=True, null=True)
    closed_at = models.DateTimeField(blank=True, null=True)
    
    issue = models.TextField()
    resolution = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

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

class Scrap(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='scraps')
    STATUS_SCRAP_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
    ]
    status = models.CharField(max_length=100, choices=STATUS_SCRAP_CHOICES, default='open')
    number = models.CharField(max_length=100, blank=True, null=True)
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)