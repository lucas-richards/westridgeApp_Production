# Generated by Django 5.0.3 on 2024-11-07 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workorder', '0020_proditem_completed_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proditem',
            name='produced_in_time',
        ),
        migrations.RemoveField(
            model_name='proditem',
            name='setup_time',
        ),
        migrations.RemoveField(
            model_name='proditemstd',
            name='setup_time',
        ),
        migrations.AlterField(
            model_name='proditemstd',
            name='people_inline',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='proditemstd',
            name='pph',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='proditemstd',
            name='setup_time_people',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]