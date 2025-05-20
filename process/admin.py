from django.contrib import admin
from .models import Case, CustomerComplaint, Return, Credit, Category

# Register your models here.
admin.site.register(Case)
admin.site.register(Category)
admin.site.register(CustomerComplaint)
admin.site.register(Return)
admin.site.register(Credit)