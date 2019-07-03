from rest_framework.generics import ListAPIView
from rss_news.models import Article
from .serializer import ArticleSerializer,ArticleTitleSerializer
from django.db.models import Q

class ArticleListAPIView(ListAPIView):
	serializer_class=ArticleSerializer
	def get_queryset(self,*args,**kwargs):
		queryset_list=Article.objects.all()
		query=self.request.GET.get("q")
		if query:
			queryset_list=queryset_list.filter(
				Q(id=query)
				).distinct()
		return queryset_list




class ArticleTitleListAPIView(ListAPIView):
	queryset=Article.objects.all()
	serializer_class=ArticleTitleSerializer