from django.contrib import admin
from django import forms
from .models import Source, Quote


class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        source = cleaned_data.get('source')
        text = cleaned_data.get('text')

        if not source:
            raise forms.ValidationError("Выберите источник цитаты")

        # проверка на максимальное количество цитат у источника
        if source and source.quotes.count() >= 3:
            raise forms.ValidationError(
                f'У источника "{source}" уже максимальное количество цитат (3)'
            )

        return cleaned_data


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'quotes_count')
    search_fields = ('name',)


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    form = QuoteForm
    list_display = ('short_text', 'source', 'weight', 'views', 'likes')
    list_editable = ('weight',)
    list_filter = ('source',)
    search_fields = ('text', 'source__name')
    readonly_fields = ('views', 'likes', 'dislikes', 'created_at')

    def short_text(self, obj):
        return obj.text[:50] + "..." if len(obj.text) > 50 else obj.text
    short_text.short_description = "Текст цитаты"
