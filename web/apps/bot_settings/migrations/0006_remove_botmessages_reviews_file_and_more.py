# Generated by Django 4.2.1 on 2025-04-03 14:20

from django.db import migrations, models
import web.validators.file


class Migration(migrations.Migration):

    dependencies = [
        ('bot_settings', '0005_botmessages_enter_info_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='botmessages',
            name='reviews_file',
        ),
        migrations.AddField(
            model_name='botmessages',
            name='reviews_file_1',
            field=models.FileField(default=1, upload_to='', validators=[web.validators.file.FileValidator(allowed_extensions=('.mp4', '.jpg', '.jpeg', '.png'))], verbose_name='Видео/Фото отзывов 1'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='botmessages',
            name='reviews_file_2',
            field=models.FileField(default=1, upload_to='', validators=[web.validators.file.FileValidator(allowed_extensions=('.mp4', '.jpg', '.jpeg', '.png'))], verbose_name='Видео/Фото отзывов 2'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='botmessages',
            name='reviews_file_3',
            field=models.FileField(default=1, upload_to='', validators=[web.validators.file.FileValidator(allowed_extensions=('.mp4', '.jpg', '.jpeg', '.png'))], verbose_name='Видео/Фото отзывов 3'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='botmessages',
            name='reviews_file_4',
            field=models.FileField(default=1, upload_to='', validators=[web.validators.file.FileValidator(allowed_extensions=('.mp4', '.jpg', '.jpeg', '.png'))], verbose_name='Видео/Фото отзывов 4'),
            preserve_default=False,
        ),
    ]
