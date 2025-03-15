from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.template.defaultfilters import filesizeformat
import os


@deconstructible
class FileValidator:
    allowed_extensions = ('.mp4', '.mp3', '.jpg', '.jpeg', '.png')
    max_upload_size = settings.MAX_UPLOAD_FILE_SIZE

    def __init__(self, *args, **kwargs):
        self.allowed_extensions = kwargs.get('allowed_extensions', self.allowed_extensions)
        self.max_upload_size = kwargs.get('max_upload_size', self.max_upload_size)

    def __call__(self, value):
        ext = os.path.splitext(value.name)[1]  # Получаем расширение файла
        if not ext.lower() in self.allowed_extensions:
            raise ValidationError(
                f'Неподдерживаемый тип файла. Разрешенные типы: '
                f'{", ".join(self.allowed_extensions)}'
            )

        if value.size > self.max_upload_size:
            raise ValidationError(
                f'Файл слишком большой.'
                f' Максимальный размер файла: {filesizeformat(self.max_upload_size)}'
            )