# Generated by Django 4.2.1 on 2025-04-07 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meditations', '0006_meditation_file_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meditation',
            name='file_id',
            field=models.CharField(blank=True, default=None, max_length=150, null=True, verbose_name='File id'),
        ),
    ]
