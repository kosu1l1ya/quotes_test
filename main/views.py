from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Sum, F, ExpressionWrapper, FloatField
import random
from .models import Quote, Source
from .forms import QuoteForm


def home(request):
    quote_id = request.GET.get('show_quote')

    if quote_id:
        quote = get_object_or_404(Quote, id=quote_id)
    else:
        quotes = list(Quote.objects.all())
        if quotes:
            weights = [q.weight for q in quotes]
            quote = random.choices(quotes, weights=weights, k=1)[0]
            quote.views += 1
            quote.save()
        else:
            quote = None

    return render(request, 'main/home.html', {'quote': quote})


def like_quote(request, quote_id):
    quote = get_object_or_404(Quote, id=quote_id)
    quote.likes += 1
    quote.save()
    return redirect(f'/?show_quote={quote_id}')


def dislike_quote(request, quote_id):
    quote = get_object_or_404(Quote, id=quote_id)
    quote.dislikes += 1
    quote.save()
    return redirect(f'/?show_quote={quote_id}')


def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = QuoteForm()

    return render(request, 'main/add_quote.html', {'form': form})


def popular_quotes(request):
    quotes = Quote.objects.annotate(
        popularity=F('likes') - F('dislikes')
    ).order_by('-popularity')[:10]

    return render(request, 'main/popular_quotes.html', {'quotes': quotes})


def dashboard(request):
    total_quotes = Quote.objects.count()
    total_authors = Source.objects.count()
    total_views = Quote.objects.aggregate(total=Sum('views'))['total'] or 0
    total_likes = Quote.objects.aggregate(total=Sum('likes'))['total'] or 0

    top_sources = Source.objects.annotate(
        total_likes=Sum('quotes__likes')
    ).order_by('-total_likes')[:3]

    top_quote = Quote.objects.annotate(
        engagement=ExpressionWrapper(
            F('likes') * 100.0 / F('views'),
            output_field=FloatField()
        )
    ).order_by('-engagement').first()

    sort_by = request.GET.get('sort', 'quote_count')

    if sort_by == 'name':
        order_by = 'name'
    elif sort_by == 'quote_count':
        order_by = '-quote_count'
    elif sort_by == 'likes':
        order_by = '-total_likes'
    elif sort_by == 'views':
        order_by = '-total_views'
    else:
        order_by = '-quote_count'

    authors_stats = Source.objects.annotate(
        quote_count=Count('quotes'),
        total_likes=Sum('quotes__likes'),
        total_views=Sum('quotes__views'),
    ).order_by(order_by)[:10]

    context = {
        'total_quotes': total_quotes,
        'total_authors': total_authors,
        'total_views': total_views,
        'total_likes': total_likes,
        'top_sources': top_sources,
        'top_quote': top_quote,
        'authors_stats': authors_stats,
        'current_sort': sort_by,
    }
    return render(request, 'main/dashboard.html', context)
