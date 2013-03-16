"""Test models."""
from django.db import models


class JanitorTestModel(models.Model):
    content = models.TextField()

    def __unicode__(self):
        return self.content

    class Meta:
        ordering = ['content']
        verbose_name = 'Janitor Test Model'
        verbose_name_plural = 'Janitor Test Models'
