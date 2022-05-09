from django.urls import path

from . import views

urlpatterns = [
	path('add_transaction', views.add_transaction, name='add_transaction'),
	path('spend_points', views.spend_points, name='spend_points'),
	path('get_payer_balances', views.get_payer_balances, name='get_payer_balances'),
]
