# Generated by Django 4.2.7 on 2023-11-21 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication', '0013_user_session_key_alter_user_create_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='age',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='avatar_url',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='self_intro',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='create_time',
            field=models.IntegerField(default=1700574441),
        ),
    ]
