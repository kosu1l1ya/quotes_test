from django.shortcuts import render     # функция для отображения шаблонов
import random
from .models import Quote


def home(request):
    quotes = list(Quote.objects.all())
    random_quote = random.choice(quotes) if quotes else None

    if random_quote:
        random_quote.views += 1
        random_quote.save()

    return render(request, 'main/home.html', {'quote': random_quote})
