from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as django_login
from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse


def signup(request):
    # username 중복확인
    # password가 맞는지, 그리고 password정책에 올바른지
    # if request.method == 'POST':
    #     form = UserCreationForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('/accounts/login/')
    # else:
    #     form = UserCreationForm()

    # 위에거를 간단화 한거임
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect(settings.LOGIN_URL)



    context = {
        'form': form
    }
    return render (request, 'registration/signup.html', context)

def login(request):
    form = AuthenticationForm(request, request.POST or None)

    if form.is_valid():
        django_login(request, form.get_user())
        return redirect(reverse('blog_list'))

    context = {
        'form': form
    }
    return render(request, 'registration/login.html', context)

