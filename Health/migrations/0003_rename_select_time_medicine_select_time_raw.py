# Generated by Django 4.2.5 on 2023-12-04 16:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Health', '0002_medicine_unit'),
    ]

    operations = [
        migrations.RenameField(
            model_name='medicine',
            old_name='select_time',
            new_name='select_time_raw',
        ),
    ]