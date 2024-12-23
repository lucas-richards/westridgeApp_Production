# Generated by Django 5.0.3 on 2024-10-21 15:43

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workorder', '0010_workorder_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workorder',
            name='recurrence',
            field=models.CharField(choices=[('Once', 'Once'), ('Daily', 'Daily'), ('Weekly', 'Weekly'), ('Monthly', 'Monthly'), ('Quarterly', 'Quarterly'), ('Biannually', 'Biannually'), ('Yearly', 'Yearly')], default='once', max_length=20),
        ),
        migrations.CreateModel(
            name='CheckListItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('pass', 'Pass'), ('fail', 'Fail'), ('flag', 'Flag')], max_length=6)),
                ('due_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('attachments', models.FileField(blank=True, null=True, upload_to='records')),
                ('notes', models.TextField(blank=True, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('workorder_record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workorder.workorderrecord')),
            ],
        ),
    ]
