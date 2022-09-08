from django.urls import path
from . import views


urlpatterns = [
    path('reviews/', views.ReviewListView.as_view(), name='reviews'),
    path('reviews/helpful/', views.ReviewHelpfulView.as_view(), name='helpful_review'),
    path('reviews/<int:id>/', views.ReviewDetailView.as_view(), name='review_detail'),
    path('reviews/create/', views.ReviewCreateView.as_view(), name='create'),
    path('reviews/update/<int:id>/', views.ReviewUpdateView.as_view(), name='update'),
    path('reviews/delete/<int:id>/', views.delete, name='delete'),
    path('create_test/', views.CreateTest.as_view(), name='create_test'),
    path('reviews/helpful/<int:id>/', views.helpful, name='helpful'),
    path('reviews/filter/country/<str:key>/', views.country_search, name='country_search'),
    path('reviews/filter/state/<str:key>/', views.state_search, name='state_search'),
    path('reviews/filter/city/<str:key>/', views.city_search, name='city_search'),
]
