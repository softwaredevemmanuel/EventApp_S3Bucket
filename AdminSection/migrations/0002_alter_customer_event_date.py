# Generated by Django 4.2.3 on 2023-07-15 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AdminSection', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='event_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]