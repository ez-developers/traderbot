from django.urls import path
from . import views


urlpatterns = [
    path('adduser/', views.userAdd.as_view(), name='adduser'),
    path('users/', views.usersList.as_view(), name="users"),
    path('users/<int:pk>/', views.userGet.as_view(), name="user"),
    path('portfolios/', views.portfoliosList.as_view(), name="portfolios"),
    path('portfolios/<int:pk>/', views.portfolioDetail.as_view(), name="portfolio"),
    path('promocodes/', views.promoList.as_view(), name="promos"),
    path('promocodes/<int:pk>/', views.promoDetail.as_view(), name="promo"),
]
