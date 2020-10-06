from django.shortcuts import render
from django.views import View
from django.conf import settings
from django.shortcuts import render, redirect
# Create your views here.
import json
import datetime
import random


class IndexView(View):
    def get(self, request, *args, **kwargs):
        return redirect('/news/')


class NewsView(View):
    def get(self, request, *args, **kwargs):
        with open(settings.NEWS_JSON_PATH, "r", encoding='utf-8') as json_file:
            json_list = json.load(json_file)
            if request.GET.get('q'):
                json_list = list(filter(
                    lambda x: request.GET.get('q') in x['title'], json_list
                ))
            return render(request, 'news.html', context={'news_list': json_list})


class NewsPageView(View):
    def get(self, request, link, *args, **kwargs):
        with open(settings.NEWS_JSON_PATH, "r", encoding='utf-8') as json_file:
            for line in json.load(json_file):
                if line['link']== int(link):
                    return render(request, 'newspage.html', context={'news': line})

class NewsCreate(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'create.html')
    def post(self, request, *args, **kwargs):
        post_dict={
            'created': str(datetime.datetime.now())[:-7],
            'text': request.POST.get('text'),
            'title': request.POST.get('title'),
            'link': random.randrange(10000, 1000000)
        }
        with open(settings.NEWS_JSON_PATH, 'a+', encoding='utf-8') as json_file:
            json_file.seek(json_file.tell()-1)
            json_file.truncate()
            json_file.write(','+json.dumps(post_dict, indent=2)+']')
        return redirect('/news/')