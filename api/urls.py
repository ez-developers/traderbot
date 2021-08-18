from django.urls import path
from . import views


urlpatterns = [
    path('adduser/', views.UserAdd.as_view(), name='adduser'),
    path('users/', views.UsersList.as_view(), name="users"),
    path('users/<int:pk>/', views.UserGet.as_view(), name="user"),
    path('portfolios/', views.PortfoliosList.as_view(), name="portfolios"),
    path('portfolios/<int:pk>/', views.PortfolioDetail.as_view(), name="portfolio"),
    path('promocodes/', views.PromoList.as_view(), name="promos"),
    path('promocodes/<int:pk>/', views.PromoDetail.as_view(), name="promo"),
    path('videos/', views.VideoLessonList.as_view(), name="videos"),
    path('videos/<int:pk>/', views.VideoLessonDetail.as_view(), name="video")
]
