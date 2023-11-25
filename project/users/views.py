from django.contrib.auth import authenticate, login
from django.views import View
from django.shortcuts import render, redirect
from users.forms import UserCreationForm
from news.models import Articles
from news.models import Like

class Register(View):

    template_name = 'registration/register.html'

    def get(self, request):
        context = {
            'form': UserCreationForm()
        }

        return render(request, self.template_name, context)

    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
        context = {
            'form': form
        }
        return render(request, self.template_name, context)


def profile_user(request, username):
    news = Articles.objects.all()
    like_news = Like.objects.all()
    return render(request, 'users/profile_user.html', {'news': news,
                                                       'like_news': like_news})