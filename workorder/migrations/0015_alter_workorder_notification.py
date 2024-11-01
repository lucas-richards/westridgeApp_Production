# Generated by Django 5.0.3 on 2024-10-30 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workorder', '0014_alter_checklistitem_workorder_record'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workorder',
            name='notification',
            field=models.CharField(choices=[('none', 'None'), ('day of event', 'Day Of Event'), ('day before', 'Day Before'), ('week before', 'Week Before'), ('month before', 'Month Before')], default='none', max_length=20),
        ),
    ]