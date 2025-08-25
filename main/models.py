from django.db import models
from django.core.exceptions import ValidationError


class Source(models.Model):     # модель для хранения источника цитаты
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

    def quotes_count(self):    # считаем сколько цитат у этого источника
        return self.quotes.count()


class Quote(models.Model):     # модель для хранения цитат
    text = models.TextField(
        verbose_name="Текст цитаты",
        unique=True)    # избегание повторения цитат
    source = models.ForeignKey(     # связь с источником
        Source,
        on_delete=models.CASCADE,     # удаляем цитаты если удален источник
        related_name='quotes',       # у источника будет quotes для доступа к цитатам
        verbose_name="Источник")
    weight = models.PositiveIntegerField(     # поле для веса цитаты
        default=1,
        verbose_name="Вес цитаты",
        help_text="Чем выше вес, тем чаще цитата показывается")
    views = models.PositiveIntegerField(    # поле для счетчика просмотров
        default=0,
        verbose_name="Просмотры")
    likes = models.PositiveIntegerField(    # поле для счетчика лайков
        default=0,
        verbose_name="Лайки")
    dislikes = models.PositiveIntegerField(    # поле для счетчика дизлайков
        default=0,
        verbose_name="Дизлайки")
    created_at = models.DateTimeField(    # поле для даты создания
        auto_now_add=True,
        verbose_name="Дата создания")

    class Meta:
        verbose_name = "Цитата"
        verbose_name_plural = "Цитаты"
        ordering = ['-created_at']    # новые сверху
        # текст + источник должны быть уникальными
        unique_together = ['text', 'source']

    def clean(self):    # проверяем данные перед сохранением
        # проверяем ограничение в 3 цитаты на источник (по заданию)
        if not self.pk:
            if self.source.quotes.count() >= 3:
                raise ValidationError(
                    f'У источника "{self.source}" уже максимальное количество цитат (3)')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'"{self.text[:50]}..." - {self.source}'

    def popularity(self):    # считаем рейтинг цитаты
        return self.likes - self.dislikes
