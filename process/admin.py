from django.contrib import admin
from .models import Case, CustomerComplaint, Return, Credit, Category, Scrap, File, Item

# Register your models here.
admin.site.register(Case)
admin.site.register(Category)
admin.site.register(CustomerComplaint)
admin.site.register(Return)
admin.site.register(Credit)
admin.site.register(Scrap)
admin.site.register(File)
admin.site.register(Item)
