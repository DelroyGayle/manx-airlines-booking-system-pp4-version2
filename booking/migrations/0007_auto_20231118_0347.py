# Generated by Django 3.2.23 on 2023-11-18 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0006_auto_20231118_0328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passenger',
            name='wheelchair_ssr',
            field=models.CharField(blank=True, default='', max_length=1),
        ),
        migrations.AlterField(
            model_name='passenger',
            name='wheelchair_type',
            field=models.CharField(blank=True, default='', max_length=1),
        ),
    ]
