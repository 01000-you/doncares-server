# Generated by Django 3.2.20 on 2023-08-05 04:07

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0006_alter_customer_app_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='app_user_id',
            field=models.PositiveIntegerField(default=1, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='driver',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='driver',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='driver',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='driver',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
