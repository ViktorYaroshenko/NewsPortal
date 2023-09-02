from django.urls import path
from .views import *
from django.views.decorators.cache import cache_page


urlpatterns = [
    path('', cache_page(60)(PostList.as_view()), name = 'posts'),
    path('<int:pk>', PostDetail.as_view(), name = 'post'),
    path('search/', PostSearch.as_view(), name = 'search'),
    path('news/create/', NewsCreate.as_view(), name = 'news_create'),
    path('articles/create/', ArticlesCreate.as_view(), name = 'articles_create'),
    path('news/<int:pk>/edit/', PostEdit.as_view(), name='post_edit'),
    path('articles/<int:pk>/edit/', PostEdit.as_view(), name='post_edit'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('articles/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('subscriptions/', subscriptions, name='subscriptions'),
]