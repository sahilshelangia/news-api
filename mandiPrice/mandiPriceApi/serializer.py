from rest_framework.serializers import ModelSerializer
from mandiPrice.models import MandiPrice

class MandiPriceApi(ModelSerializer):
	class Meta:
		model=MandiPrice
		fields='__all__'