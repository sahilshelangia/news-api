from rest_framework.generics import ListAPIView
from rss_news.models import Article
from .serializer import ArticleSerializer
class ArticleListAPIView(ListAPIView):
	queryset=Article.objects.all()
	serializer_class=ArticleSerializer