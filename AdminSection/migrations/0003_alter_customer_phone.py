# Generated by Django 4.2.3 on 2023-07-15 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AdminSection', '0002_alter_customer_event_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='phone',
            field=models.BigIntegerField(),
        ),
    ]
