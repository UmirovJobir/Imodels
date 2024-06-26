from django import forms
from django.db import models
from django.urls import reverse
from django.forms import widgets
from django.contrib import admin
from datetime import datetime, timedelta
from django.utils.html import format_html
from django.templatetags.static import static
from django_summernote.admin import SummernoteModelAdmin

from nested_admin import NestedModelAdmin
from rangefilter.filters import DateRangeQuickSelectListFilterBuilder
from modeltranslation.admin import TranslationAdmin
from libs.currency import get_currency
from .admin_filters import CategoryFilter, ProductFilter
from .admin_inlines import (
    ProductImageInline,
    ProductVideoInline,
    ProductFeatureInline,
    ProductGalleryInline,
    ItemInline,
    OrderProductInline,
    DescriptionInline,
    DescriptionPointInline,
)
from .models import (
    Category,
    Product,
    Description,
    Blog,
    ContactRequest,
    Type,
    Order,
    Sale,
    Item,
)

admin.site.site_header = "Imodels adminpanel"
admin.site.site_title = "Imodels adminpanel"
admin.site.index_title = "Imodels"


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'product', 'item']
    list_display_links = ['id', 'product']
    search_fields = ['id', 'product__title']
    list_per_page = 20


@admin.register(Type)
class TypeAdmin(TranslationAdmin):
    list_display = ['id', 'name_uz', 'name_ru', 'name_en']
    list_display_links = ['id', 'name_uz']
    search_fields = ['id', 'name_uz', 'name_ru', 'name_en']
    list_per_page = 20


@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'phone', 'message_short', 'created_at', 'status']
    list_display_links = ['id', 'name']
    list_per_page = 20
    readonly_fields = ['created_at']
    list_filter = ['status']

    def created_at(self, obj: ContactRequest) -> str:
        return obj.created_at.strftime("%d.%m.%Y, %H:%M")

    def message_short(self, obj: ContactRequest) -> str:
        if obj.message:
            if len(obj.message) < 48:
                return obj.message
            else:
                return obj.message[:48] + "..."
        return None


@admin.register(Blog)
class BlogAdmin(TranslationAdmin, SummernoteModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': forms.TextInput(attrs={'size': 170})},
    }

    list_display = ['id', 'title', 'description_short', 'popular', 'preview_image_tag']
    list_display_links = ['id', 'title']
    summernote_fields = ['text']
    readonly_fields = ['preview_image_tag']
    list_per_page = 10
    fieldsets = [
        (None, {
            "fields": [
                "popular",
                "preview_image_tag",
                "preview_image",
                "title",
                "description",
                "text",
            ]
        }
         )
    ]

    def preview_image_tag(self, obj):
        preview_image = obj.preview_image.url
        return format_html('<img src="%s" width="100px"/>' % (preview_image))

    preview_image_tag.short_description = "Rasm"

    def description_short(self, obj: Blog) -> str:
        if obj.description:
            if len(obj.description) < 48:
                return obj.description
            else:
                return obj.description[:48] + "..."
        else:
            return obj.description


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ['id', 'name_uz', 'name_ru', 'name_en', 'parent_name', 'product_count']
    list_display_links = ['id', 'name_uz']
    raw_id_fields = ['parent']
    list_filter = [CategoryFilter]
    fieldsets = [
        ("КАТЕГОРИЯ", {
            "fields": ("parent", "name"),
            "classes": ("collapse"),
            "description": "Родительская категория",
        }),
    ]

    def parent_name(self, obj):
        return obj.parent.name_uz if obj.parent else None

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('parent').prefetch_related('products')
        return queryset


# @admin.register(Description)
# class DescriptionAdmin(TranslationAdmin):
#     formfield_overrides = {
#         models.CharField: {'widget': forms.Textarea(attrs={'cols': 70, 'rows': 10})},
#     }
#     list_display = ['id', 'title_uz']
#     list_display_links = ['id', 'title_uz']
#     inlines = [DescriptionPointInline]

#     def get_queryset(self, request):
#         queryset = super().get_queryset(request)
#         queryset = queryset.prefetch_related('description_points')
#         return queryset

@admin.register(Product)
class ProductAdmin(TranslationAdmin, NestedModelAdmin, SummernoteModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': forms.TextInput(attrs={'size': 193})},
        models.IntegerField: {'widget': forms.TextInput(attrs={'size': 10})},
        models.BooleanField: {'widget': widgets.NullBooleanSelect(attrs={
            'style': 'padding: 4px 8px; border-radius: 5px; width: 100px'
        })
        },
    }

    summernote_fields = ['information']

    list_per_page = 10
    list_display = ['first_image', 'id', 'title', 'order_by', 'category_name', 'price_table', 'status']
    list_display_links = ['id', 'title']
    readonly_fields = ['id', 'price_table', 'first_image']
    raw_id_fields = ["category", "configurator"]
    list_filter = [ProductFilter]
    search_fields = ['title_uz', 'title_ru', 'title_en']
    inlines = [
        ProductImageInline,
        ProductVideoInline,
        ProductGalleryInline,
        DescriptionInline,
        ProductFeatureInline,
        ItemInline,
    ]
    fieldsets = [
        (None, {
            "fields": [
                "id",
                "price_table",
                "first_image",
            ]
        }),
        ("Konfigurator", {
            "fields": [
                "configurator",
                "is_configurator",
            ]
        }),
        ("Mahsulot", {
            "fields": [
                "status",
                "order_by",
                "category",
                "price",
            ],
            "classes": ["wide"],
        }),
        ("Sarlavha", {
            "fields": [
                "title",
            ]
        }),
        ("Informatsiya", {
            "fields": [
                "information",
            ]
        }),
    ]

    def price_table(self, obj):
        if obj.price:
            price = get_currency(obj_price=obj.price)
            return format_html(f""" 
                                <table>
                                    <tr>
                                        <th>USD</th>
                                        <th>{int(price['usd']):,.2f}</th>
                                    </tr>
                                    <tr>
                                        <th>EUR</th>
                                        <th>{int(price['eur']):,.2f}</th>
                                    </tr>
                                    <tr>
                                        <th>UZS</th>
                                        <th>{int(price['uzs']):,.2f}</th>
                                    </tr>
                                </table>
                                """
                               )
        else:
            return "-"

    price_table.short_description = "Narx jadvali"

    def category_name(self, obj: Product) -> str:
        category_tags = ''.join([
            '<a href="{}">{}</a><br>'.format(reverse('admin:shop_category_change', args=[category.pk]), category.name)
            for category in obj.category.all()])
        return format_html(category_tags)

    category_name.short_description = "Kategoriya nomi"

    def description_short(self, obj: Product) -> str:
        if len(obj.description) < 48:
            return obj.description
        else:
            return obj.description[:48] + "..."

    def first_image(self, obj):
        try:
            first_image = obj.product_images.first().image.url
        except AttributeError:
            first_image = static("img/no-image.png")
        return format_html('<img src="%s" width="100px"/>' % (first_image))

    first_image.short_description = "Rasm"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.prefetch_related('product_images', 'items', 'item', 'item__type', 'category',
                                             'product_galleries') \
            .select_related('configurator', 'product_video', 'product_features', 'product_description')
        return queryset


@admin.register(Order)
class OrderAdmin(NestedModelAdmin):
    formfield_overrides = {
        models.ForeignKey: {'widget': widgets.Input(attrs={
            'style': 'width: 90px; border-radius: 5px;'
        })
        },
        models.BooleanField: {
            'widget': widgets.NullBooleanSelect(attrs={
                'style': 'width: 100px; background-color: red;'  # 'padding: 4px 8px; border-radius: 5px;'
            })
        }
    }
    list_display = ['id', 'customer', 'formatted_total_price', 'created_at', 'order_status']
    list_display_links = ['id', 'customer', 'order_status']
    readonly_fields = ['formatted_total_price', 'first_name', 'last_name', 'phone', 'order_status', 'created_at']
    inlines = [OrderProductInline]
    raw_id_fields = ['customer']
    list_per_page = 15
    list_filter = (
        ('status'),
        ("created_at", DateRangeQuickSelectListFilterBuilder(
            title="Kun bo'yichas salarash",
            default_start=datetime.now(),  # - timedelta(days=1),
            default_end=datetime.now()
        )),
    )
    fieldsets = [
        ("Order", {
            "fields": [
                "order_status",
                "status",
                "customer",
                "phone",
                "first_name",
                "last_name",
                "created_at",
                "formatted_total_price",
            ],
        }),
    ]

    def phone(self, obj):
        return obj.customer.phone

    def first_name(self, obj):
        return obj.customer.first_name

    # first_name.short_description = 'First Name'

    def last_name(self, obj):
        return obj.customer.last_name

    # last_name.short_description = 'First Name'

    def formatted_total_price(self, obj):
        return "{:,.2f} So'm".format(obj.total_price)

    formatted_total_price.short_description = 'Total Price'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('customer').prefetch_related('order_products')
        return queryset

    def order_status(self, obj):
        if obj.status == "To'langan":
            background_color = '#2ea44f'
            color = '#fff'

        elif obj.status == "Yangi":
            background_color = '#fff000'
            color = '#000'

        elif obj.status == "Rad etilgan":
            background_color = '#ff0000'
            color = '#fff'

        elif obj.status == "Yetkazib berildi":
            background_color = '#808080'
            color = '#fff'

        else:
            background_color = None
            color = None

        return format_html(
            """<span 
                style="
                display: block;
                align-items: center;
                background-color: {};
                border-radius: 6px;
                color: {};
                padding: 6px 23px;
                text-align: center;
                ">{}
            </span>""",
            background_color, color, obj.status)


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['image_tag', 'id', 'product', 'discount', 'old_price', 'new']
    readonly_fields = ['new', 'old_price', 'discount', 'image_tag']
    list_display_links = ['id', 'product']
    raw_id_fields = ['product']
    list_per_page = 10

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('product')
        return queryset

    def new(self, obj):
        if obj.new_price:
            price = get_currency(obj_price=obj.new_price)
            return format_html(f"""  
                                <table>
                                    <tr>
                                        <th>USD</th>
                                        <th>{int(price['usd']):,.2f}</th>
                                    </tr>
                                    <tr>
                                        <th>EUR</th>
                                        <th>{int(price['eur']):,.2f}</th>
                                    </tr>
                                    <tr>
                                        <th>UZS</th>
                                        <th>{int(price['uzs']):,.2f}</th>
                                    </tr>
                                </table>
                                """
                               )

    new.short_description = format_html('<i class="fa-solid fa-tags"></i>Discount price')

    def old_price(self, obj):
        price = get_currency(obj_price=obj.product.price)
        return format_html(f""" 
                            <table>
                                <tr>
                                    <th>USD</th>
                                    <th>{int(price['usd']):,.2f}</th>
                                </tr>
                                <tr>
                                    <th>EUR</th>
                                    <th>{int(price['eur']):,.2f}</th>
                                </tr>
                                <tr>
                                    <th>UZS</th>
                                    <th>{int(price['uzs']):,.2f}</th>
                                </tr>
                            </table>
                            """
                           )

    def discount(self, obj):
        if obj.new_price:
            # discount = round((obj.product.price - obj.new_price) / obj.product.price * 100)
            return format_html(f"""
                            <script src="https://kit.fontawesome.com/850b43de8f.js" crossorigin="anonymous"></script>
                            <i class="fa-solid fa-tags"></i>{obj.discount}%""")

    def image_tag(self, obj):
        if obj:
            try:
                first_image = obj.product.product_images.first().image.url
            except AttributeError:
                first_image = static("img/no-image.png")
        else:
            first_image = static("img/no-image.png")
        return format_html('<img src="%s" width="100px" height="100px"/>' % (first_image))

    # def images(self, obj):
    #     try:
    #         product_images = obj.product.product_images.all()
    #         if product_images:
    #             image_html = ''
    #             for product_image in product_images:
    #                 image_html += f'<img src="{product_image.image.url}" width="100" height="100" style="margin-right: 10px;">'
    #             return format_html(image_html)
    #     except AttributeError:
    #         first_image = "/static/img/no-image.png"
    #         return mark_safe('<img src="%s" width="100px" height="100px" />'%(first_image))
