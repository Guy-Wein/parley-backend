# Generated by Django 4.1.1 on 2022-09-07 13:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_user_bank_account'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='bank_account',
        ),
    ]
