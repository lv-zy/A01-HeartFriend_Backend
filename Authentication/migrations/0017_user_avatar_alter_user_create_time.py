# Generated by Django 4.2.7 on 2023-11-22 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication', '0016_alter_user_create_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='avatars/'),
        ),
        migrations.AlterField(
            model_name='user',
            name='create_time',
            field=models.IntegerField(default=1700647899),
        ),
    ]