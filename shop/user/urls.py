from django.urls import path
from .views import *

app_name = 'user'
urlpatterns = [
    path('registration/', SignUpView.as_view(), name='registration'),
    path('login/', SignInView.as_view(), name='login'),
    path('profile/', profile_view, name='profile'),
    path('update_profile/', update_profile_view, name='update_profile'),
    path('logout/', LogOutView.as_view(), name='logout'),
    path('user_orders/', get_user_orders, name='user_orders')
]