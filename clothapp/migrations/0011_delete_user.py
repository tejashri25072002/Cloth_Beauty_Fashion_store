# Generated by Django 5.0 on 2023-12-18 15:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clothapp', '0010_customer_details'),
    ]

    operations = [
        migrations.DeleteModel(
            name='user',
        ),
    ]
