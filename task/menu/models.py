from django.db import models
from django.urls import reverse


class Menu(models.Model):
    """Модель для представления меню."""
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Название меню')

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    """Модель для представления пункта меню, который может иметь подменю."""
    menu = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Меню')
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='children',
        verbose_name='Родительский пункт')
    name = models.CharField(
        max_length=50,
        verbose_name='Название пункта')
    url = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='URL')
    named_url = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Named URL')
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядок')

    class Meta:
        ordering = ['order']
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Пункты меню'

    def get_absolute_url(self):
        """
        Возвращает абсолютный URL для данного пункта меню.
        Если указан именованный URL, используется метод reverse
        для его разрешения. В противном случае возвращает прямой URL.
        """
        if self.named_url:
            return reverse(self.named_url)
        return self.url

    def __str__(self):
        """
        Возвращает строковое представление объекта MenuItem,
        равное его названию.
        """
        return self.name
