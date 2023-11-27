from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect
from .forms import OrderForm
from cart.cart import Cart
from .models import *
from .serializers import *
from django.db.models import Q
from cart.forms import CardAddProductForm
from user.Bot import sendMessageTg

from django.core.paginator import Paginator


from rest_framework import  viewsets,filters
from rest_framework.permissions import AllowAny
from .pagination import PagesPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser,IsAuthenticatedOrReadOnly,AllowAny





class PlantsViewSet(viewsets.ModelViewSet):
    
    queryset = Plant.objects.select_related('category').all()
    serializer_class = PlantsSerializer
    pagination_class = PagesPagination
    permission_classes = [IsAdminUser,IsAuthenticatedOrReadOnly]

    filterset_fields = ['category']

    @action(methods=['GET'], detail=False)
    def get_check_cactuses_palms_count(self, request, **kwargs):
        #  кастомный фильтр для нужд бизнеса
        queryset = self.get_queryset().filter(~Q(category__cat_name='инструменты') & (Q(category__cat_name='пальмы') | Q(category__cat_name='кактусы')))
        data = dict()
        data['data'] = queryset.count()
        return Response(data)

    @action(methods=['POST','GET'], detail=True)
    def reset_prices(self, request, **kwargs):
        plant = self.get_object()
        plant.price = 0
        plant.old_price = 0
        plant.save()
        return Response('Цены сброшены!')
        
        
       


class OrdersViewSet(viewsets.ModelViewSet):

    queryset = Order.objects.prefetch_related('plants').all()
    serializer_class = OrdersSerializer
    pagination_class = PagesPagination
    permission_classes = [AllowAny]

    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['telegram_name']
    ordering_fields = ['id']

    @action(methods=['GET'], detail=False)
    def get_Moscow_or_Piter_exlcude_ramenskoe_orders(self, request, **kwargs):
        queryset = self.get_queryset().filter(~Q(city="Раменское") & (Q(city="Москва") | Q(city="Санкт-Петербург")))
        serializer = OrdersSerializer(queryset,many=True)
        data = dict()
        data['data'] = serializer.data
        return Response(data)
    
   
    
    







# Create your views here.
def plants_list(request):
    search_query = request.GET.get('search', '')
    categories = Category.objects.all()
    if search_query:
        plants = Plant.objects.filter(Q(plant_name__iregex=search_query) |
                                      Q(category__cat_name__iregex=search_query)).select_related('category')
    else:
        plants = Plant.objects.select_related("category").only('plant_name',
                'old_price', 'price', 'short_description', 'main_img', 'category')
    p = Paginator(plants, 6)
    page = request.GET.get('page')
    page_obj = p.get_page(page)

    dict = {

        'plants': page_obj,
        'categories': categories,
        'cat_selected': 0,
    }
    return render(request, 'main/plants_list.html', dict)


def plants_detail(request, pk):
    plant = Plant.objects.filter(pk=pk).select_related('category').first()

    cart_product_form =CardAddProductForm()
    img_gallery = PlantPhotos.objects.filter(plant=plant).only('images')
    dict = {
        'plant': plant,
        'img_gallery':img_gallery,
        'cart_product_form':cart_product_form

    }
    return render(request, 'main/plants_detail.html',dict)



def PageNofFound(request,exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

def show_category(request, cat_pk):
    plants = Plant.objects.filter(category_id=cat_pk).select_related('category')
    categories = Category.objects.all()

    if len(plants) == 0:
        raise Http404()
    dict = {
        'plants': plants,
        'categories': categories,
        'cat_selected': cat_pk,
    }
    return render(request, 'main/plants_list.html', dict)
@login_required

def create_order(request):
    cart = Cart(request)
    user = request.user

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = user  # Установка текущего пользователя как создателя заказа
            order.save()


            order_items = []
            for item in cart:
                plant = item['product']
                quantity = item['quantity']
                price = item['price']
                order_item = OrderItem(order=order, plant=plant, price=price, quantity=quantity)
                order_items.append(order_item)

            OrderItem.objects.bulk_create(order_items)  # Создание всех элементов заказа одним запросом
            order_id = order.id

            sendMessageTg(order)  # Отправить сообщение после создания всех товаров в заказе

            cart.clear()  # Очистка корзины

            return render(request, 'main/order_successful_created.html',
                          {'order_id': order_id})  # Перенаправление на страницу подтверждения заказа
    else:
        initial_data = {'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}
        form = OrderForm(initial=initial_data,
                         instance=Order(user=user))  # Передача начальных данных и экземпляра модели Order в форму

    return render(request, 'main/create_order.html', {'form': form, 'cart': cart})
