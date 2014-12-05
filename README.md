TL;DR News: Automatic Summarization of News Articles
=====================================================

Uses a combination of graph-based algorithms and semantic similarity measures (from WordNet) to perform extractive summarization.

Requirements
----------------------
  * [NetworkX](https://networkx.github.io/)
  * [NLTK](http://www.nltk.org/)
  * [NumPy](http://www.numpy.org/)
  * [scikit-learn](http://scikit-learn.org/stable/)
  * [Goose](https://github.com/grangier/python-goose)
  * [Django](https://docs.djangoproject.com/en/1.7/intro/install/)

Usage
-----
#### Web App
The TLDR summarizer web app is now hosted [here] (http://news-article-summarizer.herokuapp.com/)

#### Chrome Extension
The browser extension is available for download from the Chrome Webstore [here] (https://chrome.google.com/webstore/detail/tldr-news-article-summari/omnkfiggdjenoclnfdhijodllleflpjk). Currently supports only [NYTimes]("http://www.nytimes.com/").
     
#### Testing
Run the django app inside the [app](https://github.com/abhishekpant93/news-article-summarizer/tree/master/app) folder by executing  
     `python manage.py runserver`

Developers
----------
Abhishek Pant  
Aniruddha Gupta  
Ankit Jain  
Bhaskar Bagchi  
Shushman Chowdhary  
Rishi Rajiv Mehta  
Utkarsh Jaiswal