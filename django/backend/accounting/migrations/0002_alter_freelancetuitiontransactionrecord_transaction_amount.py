# Generated by Django 4.2.13 on 2025-03-15 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='freelancetuitiontransactionrecord',
            name='transaction_amount',
            field=models.PositiveSmallIntegerField(editable=False),
        ),
    ]
