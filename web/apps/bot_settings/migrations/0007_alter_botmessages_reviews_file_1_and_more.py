# Generated by Django 4.2.1 on 2025-04-03 15:19

from django.db import migrations, models
import web.validators.file


class Migration(migrations.Migration):

    dependencies = [
        ('bot_settings', '0006_remove_botmessages_reviews_file_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='botmessages',
            name='reviews_file_1',
            field=models.FileField(blank=True, default=None, null=True, upload_to='', validators=[web.validators.file.FileValidator(allowed_extensions=('.mp4', '.jpg', '.jpeg', '.png'))], verbose_name='Видео/Фото отзывов 1'),
        ),
        migrations.AlterField(
            model_name='botmessages',
            name='reviews_file_2',
            field=models.FileField(blank=True, default=None, null=True, upload_to='', validators=[web.validators.file.FileValidator(allowed_extensions=('.mp4', '.jpg', '.jpeg', '.png'))], verbose_name='Видео/Фото отзывов 2'),
        ),
        migrations.AlterField(
            model_name='botmessages',
            name='reviews_file_3',
            field=models.FileField(blank=True, default=None, null=True, upload_to='', validators=[web.validators.file.FileValidator(allowed_extensions=('.mp4', '.jpg', '.jpeg', '.png'))], verbose_name='Видео/Фото отзывов 3'),
        ),
        migrations.AlterField(
            model_name='botmessages',
            name='reviews_file_4',
            field=models.FileField(blank=True, default=None, null=True, upload_to='', validators=[web.validators.file.FileValidator(allowed_extensions=('.mp4', '.jpg', '.jpeg', '.png'))], verbose_name='Видео/Фото отзывов 4'),
        ),
    ]
