# Generated by Django 5.1.6 on 2025-02-24 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='entities',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
