# Generated by Django 3.2.20 on 2023-08-05 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0005_auto_20230801_1152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='app_user_id',
            field=models.PositiveIntegerField(unique=True),
        ),
    ]