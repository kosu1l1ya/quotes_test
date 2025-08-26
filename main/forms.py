from django import forms
from .models import Quote, Source


class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ['text', 'source', 'weight']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'weight': forms.NumberInput(attrs={'min': 1, 'value': 1}),
        }
        labels = {
            'text': 'Текст цитаты',
            'source': 'Источник',
            'weight': 'Вес цитаты',
        }
        help_texts = {
            'weight': 'Чем выше вес, тем чаще цитата показывается',
        }

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get('text')
        source = cleaned_data.get('source')

        if text and source:
            # проверка повторов
            if Quote.objects.filter(text=text, source=source).exists():
                raise forms.ValidationError(
                    'Такая цитата уже существует для этого источника.')

            if source.quotes.count() >= 3:      # проверка максимального количества цитат у источника
                raise forms.ValidationError(
                    'У этого источника уже максимальное количество цитат (3).')

        return cleaned_data
