# Generated by Django 3.2.16 on 2023-01-28 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stationery_management', '0002_cost_document'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cost',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]