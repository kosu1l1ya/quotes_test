from django.shortcuts import render, redirect, get_object_or_404
import random
from .models import Quote


def home(request):
    quotes = list(Quote.objects.all())
    if quotes:
        weights = [q.weight for q in quotes]
        random_quote = random.choices(quotes, weights=weights, k=1)[0]
        random_quote.views += 1
        random_quote.save()
    else:
        random_quote = None

    return render(request, 'main/home.html', {'quote': random_quote})


def like_quote(request, quote_id):
    quote = get_object_or_404(Quote, id=quote_id)
    quote.likes += 1
    quote.save()
    return redirect('home')


def dislike_quote(request, quote_id):
    quote = get_object_or_404(Quote, id=quote_id)
    quote.dislikes += 1
    quote.save()
    return redirect('home')
