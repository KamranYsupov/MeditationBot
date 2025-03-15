from django.db import models
from django.utils.translation import gettext_lazy as _

from web.db.model_mixins import (
    AsyncBaseModel,
    SingletonModelMixin,
)


class Links(AsyncBaseModel, SingletonModelMixin):
    """Singleton модель ссылок"""

    channel_link = models.URLField(_('Ссылка на канал'))
    manager_link = models.URLField(_('Ссылка на аккаунт менеджера'))