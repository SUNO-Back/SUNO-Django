# CBV
# Class Based View는
# model 넣고 template_name에 html을 지정만 해주면 자동으로 pk로 값을 가져옴.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.forms import BlogForm, CommentForm
from blog.models import Blog, Comment


class BlogListView(ListView):
    # model = Blog    => 이렇게 가져오면 무조건 Blog.objects.all() 이렇게 가져오기 때문에 밑에거로 바꾼것
    # ordering = ('-created_at', ) => 그냥 이거 붙여주면 사용 가능하긴 함
    queryset = Blog.objects.all().order_by('-created_at')
    template_name = 'blog_list.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()

        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) |
                Q(content__icontains=q)
            )
        return queryset

class BlogDetailView(ListView):
    model = Comment
    # queryset = Blog.objects.all().prefetch_related('comment_set', 'comment_set__author')
    template_name = 'blog_detail.html'
    paginate_by = 10
    # pk_url_kwarg = 'id'   => 고유 값 즉 pk의 이름이 pk가 아닐때 이런식으로 지정해주고 클래스 안에서  id로 사용 하면 됨
    def get(self, request, *args, **kwargs):
        self.object = get_object_or_404(Blog, pk=kwargs.get('blog_pk'))
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(blog=self.object).prefetch_related('author')


    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     return queryset.filter(id__lte=50)

    # def get_object(self, queryset=None):
    #     object = super().get_object()
    #     object = self.model.objects.get(pk=self.kwargs.get('pk')) 위가 이거랑 똑같은거임
    #                                        pk 값이 url로 들어오는건 kwargs에 들어옴
    #
    #     return object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['blog'] = self.object
        return context

    def post(self, *args, **kwargs):
        comment_form = CommentForm(self.request.POST)

        if not comment_form.is_valid():
            self.object = self.get_object()
            context = self.get_context_data(object=self.object)
            context['comment_form'] = comment_form
            return self.render_to_response(context)

        if not self.request.user.is_authenticated:
            raise Http404

        comment = comment_form.save(commit=False)
        # comment.blog = self.get_object()
        comment.blog_id = self.kwargs['blog_pk']
        comment.author = self.request.user
        comment.save()

        return HttpResponseRedirect(reverse_lazy('blog:detail', kwargs={'blog_pk': self.kwargs['blog_pk']}))


class BlogCreateView(LoginRequiredMixin,CreateView):
    model = Blog
    template_name = 'blog_form.html'
    fields = ('category','title', 'content')
    # success_url = reverse_lazy('cb_blog_detail', kwargs={'pk': self.object.pk})
    # 이게 여기에 있으면 호출될때마다 또 불러와져서 효율적이지 않음. 그래서 새 def로 만들어줌

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    # def get_success_url(self):
    #     return reverse_lazy('cb_blog_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sub_title'] = '작성'
        context['btn_name'] = '생성'
        return context

class BlogUpdateView(LoginRequiredMixin,UpdateView):
    model = Blog
    template_name = 'blog_form.html'
    fields = ('category','title', 'content')

    # def get_success_url(self):
    #     return reverse_lazy('cb_blog_detail', kwargs={'pk': self.object.pk})
    # 여기서 사용하지 않고 models.py에 다른형태의 함수로 만들어놨음

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(author=self.request.user)

    # 위 아래 어떤걸 쓰든 무관함. 위에가 더 짧아서 위에거를 사용.

    # def get_object(self, queryset=None):
    #     self.object = super().get_object(queryset)
    #
    #     if self.object.author != self.request.user:
    #         raise Http404
    #     return self.object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sub_title'] = '수정'
        context['btn_name'] = '수정'
        return context

class BlogDeleteView(LoginRequiredMixin,DeleteView):
    model = Blog

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(author=self.request.user)
        return queryset.filter(author=self.request.user)

    def get_success_url(self):
        return reverse_lazy('blog:list')
