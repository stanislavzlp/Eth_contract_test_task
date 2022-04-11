from django.urls import path
from .views import TokenList, TokenTotalSupply, CreateToken

urlpatterns = [
    path('create', CreateToken.as_view(), name='create_token'),
    path('list', TokenList.as_view(), name='token_list'),
    path('total_supply', TokenTotalSupply.as_view(), name='total_supply'),
]
