# Generated by Django 3.2.23 on 2023-11-22 10:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0010_rename_pax_order_number_passenger_order_number'),
    ]

    operations = [
        migrations.RenameField(
            model_name='passenger',
            old_name='order_number',
            new_name='pax_number',
        ),
    ]
