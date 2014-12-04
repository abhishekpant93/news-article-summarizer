from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
#from tldr.utils import PageRankSummarizer, LuhnSummarizer, KeyPhraseSummarizer, CommunitySummarizer, ArticleExtractor, CombinedSummarizer
from tldr.utils import KeyPhraseSummarizer, ArticleExtractor, CombinedSummarizer
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def index(request):
    return render(request, 'tldr/index.html', {})

def summarize(request):
	if 'news_article' not in request.POST or len(request.POST['news_article']) < 1 :
		return render(request, 'tldr/index.html', { 'error_message': "News article is empty or mostly contains stop words." })
	else:
		news_article = request.POST['news_article']
		news_article = ArticleExtractor.filter_unicode(news_article)
		summary = CombinedSummarizer.summarize(news_article);
		request.session['summary'] = summary
		return HttpResponseRedirect(reverse('tldr:summary', args=()))

def summary(request):
	if 'summary' not in request.session:
		return render(request, 'tldr/index.html', { 'error_message': 'Session Expired!!' })
	else:
		summary = request.session['summary']
		del request.session['summary']
		return render(request, 'tldr/summary.html', { 'summary': summary })

@csrf_exempt
def summary_api(request):
	if 'url' not in request.POST or len(request.POST['url']) < 1 :
		return HttpResponse('No news article to summarize!!')
	else:
		url = request.POST['url']
		news_article = ArticleExtractor.parse(url)
		summary = CombinedSummarizer.summarize(news_article['text']);
		request.session['title'] = news_article['headline']
		request.session['summary'] = summary
		return HttpResponseRedirect(reverse('tldr:api_result', args=()))

def api_result(request):
	if 'summary' not in request.session:
		return HttpResponse('Session expired!!')
	else:
		summary = request.session['summary']

		s = '~'.join(summary)
		t = request.session['title']

		del request.session['summary']
		del request.session['title']

		return HttpResponse(t + '@' + s)
