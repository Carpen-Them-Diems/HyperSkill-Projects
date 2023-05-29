from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.edit import FormView
from .forms import CreateArticleForm
from django.conf import settings
from itertools import groupby
import json
from datetime import datetime


class BaseView(View):
    template_name = 'base.html'

    def get(self, request):
        return render(request, self.template_name)

    @staticmethod
    def redirect_view(*args):
        return redirect('news/')


class HomeView(View):
    template_name = 'news/news.html'

    def get(self, request):
        search_query = request.GET.get('q', '')
        news_json_path = settings.NEWS_JSON_PATH
        with open(news_json_path) as json_file:
            news_data = json.load(json_file)
            news_data = [article for article in news_data if search_query.lower() in article['title'].lower()]
            news_data.sort(key=lambda x: x['created'], reverse=True)
            grouped_articles = []
            for key, group in groupby(news_data, lambda x: x['created'][:10]):
                grouped_articles.append({
                    'date': key,
                    'articles': sorted(list(group), key=lambda x: x['title'])
                })
            context = {'grouped_articles': grouped_articles}
            return render(request, self.template_name, context)


class ArticleView(View):
    template_name = 'news/article.html'

    def get(self, request, link):
        json_path = settings.NEWS_JSON_PATH
        with open(json_path, 'r') as json_data:
            news_data = json.load(json_data)
            for article in news_data:
                if article['link'] == int(link):
                    return render(request, self.template_name, {'article': article})


class CreateArticleView(FormView):
    template_name = 'create.html'
    form_class = CreateArticleForm
    form = CreateArticleForm()
    context = {'form': form}
    # success_url = 'news/'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form = CreateArticleForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            text = form.cleaned_data['text']
            json_path = settings.NEWS_JSON_PATH
            with open(json_path, 'r+') as json_data:
                news_data = json.load(json_data)
                for article in news_data:
                    links = []
                    if article['link'] != 9234732:
                        links.append(article)
                        link = max(article['link'] for article in links) + 1
                created = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                news_data.append({
                    'created': created,
                    'text': text,
                    'title': title,
                    'link': link
                })
                json_data.seek(0)
                json.dump(news_data, json_data)
            return redirect('/news/')
        elif not form.is_valid():
            return render(request, self.template_name, self.context)
