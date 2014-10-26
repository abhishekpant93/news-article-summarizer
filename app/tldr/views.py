from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from tldr.models import Summarizer

# Create your views here.
def index(request):
    return render(request, 'tldr/index.html', {})

def summary(request):
	if 'news_article' not in request.POST or len(request.POST['news_article']) < 1 :
		return render(request, 'tldr/index.html', { 'error_message': "News article text area cannot be empty." })
	else:
		news_article = request.POST['news_article']
		summary = Summarizer.summarize(news_article);
		return render(request, 'tldr/summary.html', { 'summary': summary })

