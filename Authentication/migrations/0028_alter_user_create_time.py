# Generated by Django 4.2.7 on 2023-12-05 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication', '0027_alter_user_create_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='create_time',
            field=models.IntegerField(default=1701749948),
        ),
    ]
