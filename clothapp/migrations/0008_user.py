# Generated by Django 5.0 on 2023-12-14 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clothapp', '0007_addcart_quantity_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='user',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', models.CharField(max_length=10)),
            ],
        ),
    ]