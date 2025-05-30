# Generated by Django 5.2 on 2025-05-16 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0002_case_is_complaint_case_is_credit_case_is_return'),
    ]

    operations = [
        migrations.AddField(
            model_name='credit',
            name='number',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='customercomplaint',
            name='number',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='return',
            name='number',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='case',
            name='is_complaint',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='case',
            name='is_credit',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='case',
            name='is_return',
            field=models.BooleanField(default=True),
        ),
    ]
