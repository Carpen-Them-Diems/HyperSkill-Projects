from django.urls import path
from .views import HomeView, ArticleView, CreateArticleView, BaseView


urlpatterns = [
    path('', BaseView.redirect_view),
    path('news/', HomeView.as_view(), name='news'),
    path('news/<int:link>/', ArticleView.as_view(), name='articles'),
    path('news/create/', CreateArticleView.as_view(), name='create_article'),
]
