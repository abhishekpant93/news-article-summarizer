import requests
import goose

proxies = {
  "http": "http://10.3.100.207:8080",
  "https": "http://10.3.100.207:8080",
}

class ArticleExtractor():

    def filter_unicode(self, str):
        # str = str.replace("u'", "")
        # str = str.replace("\u201d","\"")
        # str = str.replace("\u201c", "\"")
        # str = str.replace("\u2019", "'")
        # str = str.replace("\u2018", "'")
        # str = str.replace("\u2014", " ")
        # str = str.replace("\'", "")
        # str = str.replace("\"", "")
        # str = str.replace("\n", " ")
        str = str.encode('ascii', 'ignore')
        str = str.replace("\n", " ")
        return str

    def parse(self, url):
        page = requests.get(url, proxies = proxies)
        g = goose.Goose()
        #article = g.extract(url=url)
        article = g.extract(raw_html = page.text)
        items = {}
        items['headline'] = article.title
        items['text'] = self.filter_unicode(article.cleaned_text)
        return items

def main():
    extractor = ArticleExtractor()
    url1 = "http://www.nytimes.com/2014/11/07/world/asia/another-ex-commando-says-he-shot-bin-laden.html"
    url2 = "http://news.yahoo.com/world-powers-hunker-down-ahead-crunch-iran-talks-130748461.html"
    items = extractor.parse(url2)
    print items

main()
    

