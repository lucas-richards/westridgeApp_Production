# Generated by Django 5.2 on 2025-06-03 23:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0031_item_inspected_item_inspection_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='inspection_notes',
            field=models.TextField(blank=True, null=True),
        ),
    ]
