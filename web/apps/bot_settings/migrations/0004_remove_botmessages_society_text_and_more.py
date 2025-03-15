# Generated by Django 4.2.1 on 2025-03-15 11:57

from django.db import migrations, models
import web.validators.file


class Migration(migrations.Migration):

    dependencies = [
        ('bot_settings', '0003_botmessages_about_teacher_text_botmessages_faq_text_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='botmessages',
            name='society_text',
        ),
        migrations.AddField(
            model_name='botmessages',
            name='about_teacher_video',
            field=models.FileField(upload_to='', validators=[web.validators.file.FileValidator(allowed_extensions=('.mp4',))], verbose_name='Видео об учителе'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='botmessages',
            name='society_video',
            field=models.FileField(upload_to='', validators=[web.validators.file.FileValidator(allowed_extensions=('.mp4',))], verbose_name='Видео сообщества'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='botmessages',
            name='about_teacher_text',
            field=models.TextField(max_length=4000, verbose_name='Текст об учителе'),
        ),
        migrations.AlterField(
            model_name='botmessages',
            name='faq_text',
            field=models.TextField(max_length=4000, verbose_name='Текст ответы на вопросы'),
        ),
        migrations.AlterField(
            model_name='botmessages',
            name='reviews_file',
            field=models.FileField(upload_to='', validators=[web.validators.file.FileValidator(allowed_extensions=('.mp4', '.jpg', '.jpeg', '.png'))], verbose_name='Видео/Фото отзывов'),
        ),
        migrations.AlterField(
            model_name='botmessages',
            name='reviews_text',
            field=models.TextField(max_length=4000, verbose_name='Текст отзывы'),
        ),
        migrations.AlterField(
            model_name='botmessages',
            name='useful_posts_text',
            field=models.TextField(max_length=4000, verbose_name='Текст полезные статьи'),
        ),
    ]
