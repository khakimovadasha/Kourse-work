from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import *
from django import forms
from phonenumber_field.widgets import PhoneNumberPrefixWidget
# Register your models here.
from django.utils.safestring import mark_safe
import admin_thumbnails

from simple_history.admin import SimpleHistoryAdmin
from import_export.admin import ImportExportMixin,ExportActionModelAdmin
from import_export import resources, fields,widgets
from import_export.widgets import ForeignKeyWidget
from django.db.models import Q


User = get_user_model()


#plant model
@admin_thumbnails.thumbnail('images')
class PlantsPhotosInline(admin.TabularInline):
    model = PlantPhotos
    extra = 1
    readonly_fields = ('id',)

class PlantAdmin(admin.ModelAdmin):
    list_display = ['id', 'plant_name', 'old_price', 'price', 'category', 'preview']
    list_filter = ['plant_name', 'price', 'old_price', 'category']
    list_display_links = ['id', 'plant_name']
    list_editable = ['price', 'old_price']
    inlines = [PlantsPhotosInline]

    def preview(self, obj):
        return mark_safe(f"<img src='{obj.main_img.url}'style='max-height: 80px; max-width:50px;'>")
#----------------------------------------------------


#order model
class OrderForm(forms.ModelForm):
    class Meta:
        widgets = {
            'phone_number': PhoneNumberPrefixWidget(attrs={'class': 'phone-number'}),
        }

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    readonly_fields = ('id',)

class OrderResource(resources.ModelResource):
    
    order_name = fields.Field(attribute='order_name', column_name='Имя Фамилия')
    order_plants = fields.Field(attribute='plants', column_name='Растения',widget=widgets.ManyToManyWidget(Plant, field='plant_name', separator=' '))
    user = fields.Field(
       attribute="user",
       column_name="Пользователь",
       widget=ForeignKeyWidget(User, "username")
   )
     
    class Meta:
        model = Order
       
        fields = ['id','user','order_name' ,'email','address' ,'city' ,'created','order_plants' ,'telegram_name','phone_number']
        export_order = fields
        

    def dehydrate_order_name(self, order):
        return f'{order.first_name} {order.last_name}' 
    
    def get_export_headers(self):
        headers = []
        for field in self.get_fields():
            model_fields = self.Meta.model._meta.get_fields()
            header = next((x.verbose_name for x in model_fields if x.name == field.column_name), field.column_name)
            headers.append(header)
        return headers

class OrderAdmin(ImportExportMixin,ExportActionModelAdmin,SimpleHistoryAdmin,admin.ModelAdmin):
    form = OrderForm
    list_display = ['id', 'first_name', 'last_name', 'email', 'city','telegram_name', 'created']
    date_hierarchy = 'created'
    list_editable = ['telegram_name']
    inlines = [OrderItemInline]
    list_filter = ['id', 'first_name', 'last_name', 'city']

    resource_class = OrderResource

    
    def get_export_queryset(self, request):
        return Order.objects.all().order_by('-id')


#orderitem model
class OrderItemAdmin(ImportExportMixin,ExportActionModelAdmin,SimpleHistoryAdmin,admin.ModelAdmin):
    list_display = ['order', 'plant', 'price', 'quantity', 'time_created']
    date_hierarchy = 'time_created'
    list_editable = ['price', 'quantity']
    list_filter = ['price', 'quantity', 'order']
    raw_id_fields = ['order', 'plant']
    search_fields = ['order__id', 'plant__plant_name']


class PlantPhotosAdmin(ImportExportMixin,ExportActionModelAdmin,SimpleHistoryAdmin,admin.ModelAdmin):

    list_display = ['images', 'plant', 'preview']
    def preview(self, obj):
        return mark_safe(f"<img src='{obj.images.url}'style='max-height: 80px; max-width:50px;'>")
#-----------------------------------


admin.site.register(Plant, PlantAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Category)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(PlantPhotos, PlantPhotosAdmin)