# Generated by Django 5.2 on 2025-05-28 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0019_alter_customercomplaint_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='customercomplaint',
            name='disposition_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='customercomplaint',
            name='status',
            field=models.CharField(choices=[('open', 'Open'), ('request_submitted', 'Request Submitted'), ('path_assigned', 'Path Assigned'), ('investigation_in_progress', 'Investigation In Progress'), ('disposition', 'Disposition'), ('resolution', 'Resolution'), ('closed', 'Closed')], default='open', max_length=100),
        ),
    ]
