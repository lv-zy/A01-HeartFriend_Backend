# Generated by Django 4.2.7 on 2023-12-15 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication', '0008_alter_user_create_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_forum_admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='create_time',
            field=models.IntegerField(default=1702630915),
        ),
    ]