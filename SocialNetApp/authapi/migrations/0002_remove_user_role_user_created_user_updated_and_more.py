# Generated by Django 4.2 on 2024-06-03 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapi', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='role',
        ),
        migrations.AddField(
            model_name='user',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='updated',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='Role',
        ),
    ]