from django.urls import path,include
from  .views import *
from user.views import UserViewSet
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'plants',PlantsViewSet)
router.register(r'orders',OrdersViewSet)
router.register(r'users',UserViewSet)
urlpatterns = [
    path('', plants_list, name='flower-list'),
    path('flower/<int:pk>/', plants_detail, name='flower-detail'),
    path('category/<int:cat_pk>/', show_category, name='category'),
    path('order/', create_order, name='order'),
    
    path('api/v1/',include(router.urls)),
]