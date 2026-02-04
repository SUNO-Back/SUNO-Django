from django.urls import path

from blog import cb_views

app_name = 'blog'

urlpatterns = [
    # CBV blog
    path('', cb_views.BlogListView.as_view(), name='list'),
    path('<int:blog_pk>/', cb_views.BlogDetailView.as_view(), name='detail'),
    path('create/', cb_views.BlogCreateView.as_view(), name='create'),
    path('<int:pk>/update/', cb_views.BlogUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', cb_views.BlogDeleteView.as_view(), name='delete'),
]

# html에서
# 이렇게 따로 빼서 include ursl를 적용 시키면
# {% url 'blog_list'  %} < url 'blog:list' 로 바꿔줘야 함
#                        app이름을 쓰고 그 안에서 고르는것.