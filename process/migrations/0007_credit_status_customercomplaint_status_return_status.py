# Generated by Django 5.2 on 2025-05-19 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0006_alter_case_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='credit',
            name='status',
            field=models.CharField(choices=[('open', 'Open'), ('closed', 'Closed')], default='open', max_length=100),
        ),
        migrations.AddField(
            model_name='customercomplaint',
            name='status',
            field=models.CharField(choices=[('open', 'Open'), ('quality', 'Quality'), ('customer_service', 'Customer Service'), ('sales', 'Sales'), ('warehouse', 'Warehouse'), ('production', 'Production'), ('closed', 'Closed')], default='open', max_length=100),
        ),
        migrations.AddField(
            model_name='return',
            name='status',
            field=models.CharField(choices=[('open', 'Open'), ('closed', 'Closed')], default='open', max_length=100),
        ),
    ]
