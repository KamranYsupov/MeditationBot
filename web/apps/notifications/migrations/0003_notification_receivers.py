# Generated by Django 4.2.1 on 2025-03-15 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telegram_users', '0003_telegramuser_full_name'),
        ('notifications', '0002_alter_notification_options_alter_notification_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='receivers',
            field=models.ManyToManyField(to='telegram_users.telegramuser', verbose_name='Получатели'),
        ),
    ]
