from django.shortcuts import render, redirect
from .models import Articles, Like
from .forms import ArticlesForm
from django.views.generic import DetailView, UpdateView, DeleteView
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .forms import LikeForm

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


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = get_object_or_404(Articles, pk=self.kwargs['pk'])
        context['article'] = article
        return context


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


def article_detail(request, article_id):
    article = get_object_or_404(Articles, id=article_id)
    liked = False
    like_form = LikeForm()

    if request.user.is_authenticated:
        if request.method == 'POST':
            like_form = LikeForm(request.POST)
            if like_form.is_valid():
                like, created = Like.objects.get_or_create(user=request.user, article=article)
                if not created:
                    like.delete()


                return redirect('news-detail', article_id=article.id)

        liked = Like.objects.filter(user=request.user, article=article).exists()

    return render(request, 'news/details_view.html', {'article': article, 'liked': liked, 'like_form': like_form})




