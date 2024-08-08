# Generated by Django 5.0.3 on 2024-08-07 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workorder', '0002_asset_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workorder',
            name='status',
            field=models.CharField(choices=[('in_progress', 'In Progress'), ('on_hold', 'On Hold'), ('open', 'Open'), ('done', 'Done'), ('scheduled', 'Scheduled'), ('cancelled', 'Cancelled')], default='scheduled', max_length=20),
        ),
        migrations.AlterField(
            model_name='workorderrecord',
            name='status',
            field=models.CharField(choices=[('in_progress', 'In Progress'), ('on_hold', 'On Hold'), ('open', 'Open'), ('done', 'Done'), ('scheduled', 'Scheduled'), ('cancelled', 'Cancelled')], default='open', max_length=20),
        ),
    ]