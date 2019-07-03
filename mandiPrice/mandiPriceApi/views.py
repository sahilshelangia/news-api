from rest_framework.generics import ListAPIView
from mandiPrice.models import MandiPrice
from .serializer import MandiPriceApi
from django.db.models import Q

class MandiPriceApiView(ListAPIView):
	serializer_class=MandiPriceApi
	def get_queryset(self,*args,**kwargs):
		queryset_list=MandiPrice.objects.all()
		query=self.request.GET.get("district")
		if query:
			queryset_list=queryset_list.filter(
				Q(district=query)
				).distinct()

		query=self.request.GET.get("market")
		if query:
			queryset_list=queryset_list.filter(
				Q(market=market)
				).distinct()

		query=self.request.GET.get("commodity")
		if query:
			queryset_list=queryset_list.filter(
				Q(commodity=commodity)
				).distinct()

		return queryset_list
