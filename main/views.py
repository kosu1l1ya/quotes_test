from django.shortcuts import render, redirect, get_object_or_404
import random
from .models import Quote
from .forms import QuoteForm


def home(request):
    # проверка, запрошена ли конкретная цитата через параметр url
    quote_id = request.GET.get('show_quote')

    if quote_id:        # показывается указанная цитату без увеличения счетчика просмотров
        quote = get_object_or_404(Quote, id=quote_id)
    else:       # выбирается случайная цитата с учетом веса и увеличивается счетчик просмотров
        quotes = list(Quote.objects.all())
        if quotes:
            weights = [q.weight for q in quotes]
            quote = random.choices(quotes, weights=weights, k=1)[0]
            quote.views += 1
            quote.save()
        else:
            quote = None

    return render(request, 'main/home.html', {'quote': quote})


def like_quote(request, quote_id):      # счетчик лайков увеличивается и остаётся та же цитата
    quote = get_object_or_404(Quote, id=quote_id)
    quote.likes += 1
    quote.save()
    return redirect(f'/?show_quote={quote_id}')


def dislike_quote(request, quote_id):      # аналогично с дизлайками
    quote = get_object_or_404(Quote, id=quote_id)
    quote.dislikes += 1
    quote.save()
    return redirect(f'/?show_quote={quote_id}')


def add_quote(request):     # добавление новых цитат в общий пул из интерфейса приложения
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = QuoteForm()

    return render(request, 'main/add_quote.html', {'form': form})
