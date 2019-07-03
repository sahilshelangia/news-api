from rest_framework.serializers import ModelSerializer
from rss_news.models import Article,ArticleTitle

class ArticleTitleSerializer(ModelSerializer):
	class Meta:
		model=ArticleTitle
		fields='__all__'

class ArticleSerializer(ModelSerializer):
	class Meta:
		model=Article
		fields='__all__'