# Generated by Django 3.2.9 on 2021-11-29 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='is_company_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
    ]