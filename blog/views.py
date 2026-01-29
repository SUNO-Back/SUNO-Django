from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods

from blog.models import Blog
from blog.forms import BlogForm
from django.urls import reverse


def blog_list(request):
    blogs = Blog.objects.all().order_by('-created_at')

    q = request.GET.get('q')
    if q:
        blogs = blogs.filter(
            Q(title__icontains=q) |
            Q(content__icontains=q)

        )
        # blogs = blogs.filter(content__icontains=q)

    paginator = Paginator(blogs, 10)
    page = request.GET.get('page')
    page_object = paginator.get_page(page)

    # visits = int(request.COOKIES.get('visits', 0)) + 1
    #
    # request.session['count'] = request.session.get('count',0) + 1

    context = {
        # 'blogs': blogs,
        'page_object': page_object,
    }
    return render(request, 'blog_list.html', context)

def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    context = {'blog': blog}
    return render(request, 'blog_detail.html', context)
@login_required()
def blog_create(request):
    # if not request.user.is_authenticated:
    #     return redirect(reverse('login'))
    # @login_required가 위에 코드 역할을 대신 해줌
    form = BlogForm(request.POST or None)
    if form.is_valid():
        blog = form.save(commit=False)
        blog.author = request.user
        blog.save()
        return redirect(reverse('blog_detail', kwargs={'pk': blog.pk}))


    context = {
        'form': form,
    }
    return render(request, 'blog_create.html', context)

@login_required()
def blog_update(request, pk):
    blog = get_object_or_404(Blog, pk=pk, author=request.user)
    # if request.user != blog.author:
    #     raise Http404                 => author=request.user 이 부분인거임. 글쓴이가 진짜 글쓴이가 맞는지.

    form = BlogForm(request.POST or None, instance=blog)
    if form.is_valid():
        blog = form.save()
        return redirect(reverse('blog_detail', kwargs={'pk': blog.pk}))

    context = {
        'form' : form,
    }
    return render(request, 'blog_update.html', context)

@login_required()
@require_http_methods(['POST'])
def blog_delete(request, pk):
    # if request.method != 'POST':
    #     raise Http404()           => 위에 @require_http_methods가 이 역할. 특정 메소드만 허락함
    blog = get_object_or_404(Blog, pk=pk, author=request.user)
    blog.delete()

    return redirect(reverse('blog_list'))