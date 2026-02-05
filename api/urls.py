from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('products/', views.ProductListCreateAPIView.as_view()),
    path('products/info/', views.ProductInfoAPIView.as_view()),
    path('products/<int:id>/', views.ProductDetailAPIView.as_view()),
    path('users/', views.UserListView.as_view()),
]

router = DefaultRouter()
router.register('orders', views.OrderViewset)
urlpatterns += router.urls
