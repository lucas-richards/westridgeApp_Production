# Generated by Django 5.2 on 2025-05-22 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0015_remove_case_file1_remove_case_file2_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customercomplaint',
            old_name='investigation_completed',
            new_name='time_closed',
        ),
        migrations.RenameField(
            model_name='customercomplaint',
            old_name='investigation_started',
            new_name='time_investigation_in_progress',
        ),
        migrations.RenameField(
            model_name='customercomplaint',
            old_name='quality_completed',
            new_name='time_path_assigned',
        ),
        migrations.RenameField(
            model_name='customercomplaint',
            old_name='quality_received',
            new_name='time_request_submitted',
        ),
        migrations.AddField(
            model_name='customercomplaint',
            name='time_resolution',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
