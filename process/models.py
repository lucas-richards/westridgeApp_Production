from django.db import models

# Create your models here.
class Case(models.Model):
    description = models.TextField()
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
    ]
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='open')
    category = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    is_complaint = models.BooleanField(default=True)
    is_return = models.BooleanField(default=True)
    is_credit = models.BooleanField(default=True)

    def __str__(self):
        return f"Case #{self.id}"

class CustomerComplaint(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='complaints')
    number = models.CharField(max_length=100, blank=True, null=True)
    issue = models.TextField()
    resolution = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Return(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='returns')
    number = models.CharField(max_length=100, blank=True, null=True)
    authorized = models.BooleanField(default=False)
    reason = models.TextField()
    item_condition = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

class Credit(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='credits')
    number = models.CharField(max_length=100, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    credit_reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)