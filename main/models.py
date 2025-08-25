from django.db import models
from django.core.exceptions import ValidationError


class Source(models.Model):
    name = models.CharField(
        max_length=150,
        unique=True,    # избегание дубликатов названий
        verbose_name="Название источника")

    class Meta:
        verbose_name = "Источник"
        verbose_name_plural = "Источники"
        ordering = ['name']

    def __str__(self):
        return self.name

    def quotes_count(self):
        return self.quotes.count()


class Quote(models.Model):
    text = models.TextField(
        verbose_name="Текст цитаты",
        unique=True)
    source = models.ForeignKey(
        Source,
        on_delete=models.CASCADE,
        related_name='quotes',
        verbose_name="Источник")
    weight = models.PositiveIntegerField(
        default=1,
        verbose_name="Вес цитаты",
        help_text="Чем выше вес, тем чаще цитата показывается")
    views = models.PositiveIntegerField(
        default=0,
        verbose_name="Просмотры")
    likes = models.PositiveIntegerField(
        default=0,
        verbose_name="Лайки")
    dislikes = models.PositiveIntegerField(
        default=0,
        verbose_name="Дизлайки")
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания")

    class Meta:
        verbose_name = "Цитата"
        verbose_name_plural = "Цитаты"
        ordering = ['-created_at']
        unique_together = ['text', 'source']

    def __str__(self):
        return f'"{self.text[:50]}..." - {self.source}'

    def popularity(self):
        return self.likes - self.dislikes
