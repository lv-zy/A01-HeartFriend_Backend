# Generated by Django 4.2.5 on 2023-12-04 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication', '0019_alter_user_create_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='create_time',
            field=models.IntegerField(default=1701704501),
        ),
    ]
