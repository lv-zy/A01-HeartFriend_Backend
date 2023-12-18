# Generated by Django 4.2.7 on 2023-12-17 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Administration', '0002_remove_report_is_resolved_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='report_status',
            field=models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending', max_length=50),
        ),
    ]
