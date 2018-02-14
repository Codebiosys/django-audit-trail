""" Testing-only models
"""

from django.db import models


class DummyModel(models.Model):
    """ Model specifically for testing migrations """

    class Meta:
        app_label = 'tests'

    text = models.CharField(
        max_length=100,
        verbose_name='Text comes here',
        help_text='Text description.'
    )
