from django.shortcuts import render, redirect
from .models import Articles
from .forms import ArticlesForm
from django.views.generic import DetailView, UpdateView, DeleteView
from django.utils import timezone


def news_home(request):
    news = Articles.objects.order_by('-date')
    return render(request, 'news/news_home.html', {'news': news})


class NewsDetailView(DetailView):
    model = Articles
    template_name = 'news/details_view.html'
    context_object_name = 'article'


class NewsUpdateView(UpdateView):
    model = Articles
    template_name = 'news/news-update.html'
    form_class = ArticlesForm



class NewsDeleteView(DeleteView):
    model = Articles
    success_url = '/news/'
    template_name = 'news/news-delete.html'


def create(request):
    error = ''
    if request.method == 'POST':
        form = ArticlesForm(request.POST)
        if form.is_valid():
            author_id = form.cleaned_data['author']
            article = Articles(title=form.cleaned_data['title'],
                               anons=form.cleaned_data['anons'],
                               full_text=form.cleaned_data['full_text'],
                               author=request.user)
            article.save()
            return redirect('news_home')
        else:
            error = 'Форма была неверной'
    else:
        form = ArticlesForm(initial={'date': timezone.now()})

    data = {
        'form': form,
        'error': error
    }

    return render(request, 'news/create.html', data)
