# Generated by Django 5.1.6 on 2025-03-11 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0005_remove_order_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='rating',
        ),
        migrations.AddField(
            model_name='banner',
            name='url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
