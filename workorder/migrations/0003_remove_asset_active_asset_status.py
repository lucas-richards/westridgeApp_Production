# Generated by Django 5.0.3 on 2024-07-31 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workorder', '0002_rename_estimated_time_workorder_estimated_hours'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='asset',
            name='active',
        ),
        migrations.AddField(
            model_name='asset',
            name='status',
            field=models.CharField(choices=[('online', 'Online'), ('offline', 'Offline'), ('do_not_track', 'Do Not Track')], default='online', max_length=20),
        ),
    ]