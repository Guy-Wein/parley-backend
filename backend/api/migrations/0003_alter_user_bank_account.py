# Generated by Django 4.1.1 on 2022-09-07 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_user_bank_account'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='bank_account',
            field=models.IntegerField(blank=True),
        ),
    ]