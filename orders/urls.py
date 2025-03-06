from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet


router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')


urlpatterns = [
    path('create/', views.create_order, name='create_order'),
    path('', views.order_list, name='order_list'),
    path('<int:pk>/delete/', views.delete_order, name='delete_order'),
    path('<int:pk>/update/', views.update_order, name='update_order'),
    path('api/', include(router.urls)),
    path('revenue/', views.revenue_report, name='revenue_report'),
    
]