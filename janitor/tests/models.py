"""
Test models.
"""
from django.db import models

class TestModel(models.Model):
    content = models.TextField()

    def __unicode__(self):
        return self.content

    class Meta:
        ordering = ['content']
        verbose_name = 'Test Model'
        verbose_name_plural = 'Test Models'

