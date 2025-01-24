from django.db import models


class TimeBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Когда создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Когда обновлено')

    class Meta:
        abstract = True
