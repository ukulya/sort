from django.db import models


class TimeStampedModel(models.Model):
    """
    Model template for models where need to keep created_at and updated_at data
    """

    class Meta:
        abstract = True

    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата обновления', auto_now=True)
