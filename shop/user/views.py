from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import SignUpForm, SignInForm, CustomUserForm
from django.contrib.auth.decorators import login_required
from main.models import OrderItem, Order

from .models import User
from .pagination import PagesPagination
from .filters import IsOwnerFilterBackend
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import  viewsets

class UserViewSet(viewsets.ModelViewSet):
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PagesPagination
    filter_backends = [IsOwnerFilterBackend]
    permission_classes = [IsAuthenticated]


class SignInView(LoginView):
    form_class = SignInForm
    template_name = 'user/login_form.html'
    success_url = reverse_lazy('flower-list')

    def get_success_url(self):
        return self.success_url


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('flower-list')
    template_name = 'user/register_form.html'

    def form_valid(self, form):
        form_valid = super().form_valid(form)
        username = form.cleaned_data["username"]

        password = self.request.POST['password1']
        aut_user = authenticate(username=username, password=password)
        login(self.request, aut_user)
        return form_valid

@login_required
def profile_view(request):
    user = request.user
    return render(request, 'user/profile.html', {'user': user})


def update_profile_view(request):
    user = request.user
    form = CustomUserForm(instance=user)
    if request.method == "POST":
        form = CustomUserForm(request.POST, request.FILES, instance=user)
        form.save()
        return redirect('user:profile')
    dict = {
        'form':form
    }

    return render(request, 'user/update_profile.html', dict)


class LogOutView(LogoutView):
    next_page = reverse_lazy('flower-list')






def get_user_orders(request):
    user = request.user
    orders = Order.objects.filter(user=user).prefetch_related('plants')
    ordered_plants = []

    for order in orders:
        plants = order.plants.all()
        ordered_plants.extend(plants)

    return render(request, 'user/user_order_list.html', {'user': user, 'orders': orders, 'ordered_plants': ordered_plants})