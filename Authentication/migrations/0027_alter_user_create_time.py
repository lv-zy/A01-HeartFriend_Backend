# Generated by Django 4.2.7 on 2023-12-05 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication', '0026_user_uuid_alter_user_create_time_alter_user_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='create_time',
            field=models.IntegerField(default=1701748905),
        ),
    ]
