# Generated by Django 4.2.1 on 2025-03-31 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('information', '0004_remove_topic_file_remove_topic_text_topic_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='link',
            field=models.URLField(default='https://google.com', verbose_name='Ссылка'),
        ),
    ]
