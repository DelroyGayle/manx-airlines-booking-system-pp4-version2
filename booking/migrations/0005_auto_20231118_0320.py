# Generated by Django 3.2.23 on 2023-11-18 03:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0004_auto_20231116_1342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passenger',
            name='wheelchair_ssr',
            field=models.CharField(blank=True, choices=[('', ''), ('R', 'WCHR'), ('S', 'WCHS'), ('C', 'WCHC')], default='', max_length=1),
        ),
        migrations.AlterField(
            model_name='passenger',
            name='wheelchair_type',
            field=models.CharField(blank=True, choices=[('', ''), ('M', 'WCMP'), ('L', 'WCLB'), ('D', 'WCBD'), ('W', 'WCBW')], default='', max_length=1),
        ),
    ]
