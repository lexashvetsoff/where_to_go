from django.contrib import admin
from django.utils.html import format_html

from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin, SortableAdminBase, PolymorphicSortableAdminMixin

from places.models import Place, PlaceImage


class PlaceImageInline(SortableInlineAdminMixin, admin.TabularInline):
    model = PlaceImage
    readonly_fields = ['get_preview_image']
    fields = ['place_img', 'get_preview_image']

    def get_extra(self, request, obj=None, **kwargs):
        extra = 1
        return extra
    
    def get_preview_image(self, obj):
        img_width = obj.place_img.width / 5
        img_height = obj.place_img.height / 5

        if img_height > 200:
            img_width = obj.place_img.width / 7
            img_height = obj.place_img.height / 7
        
        return format_html(f'<img src="{obj.place_img.url}" width="{img_width}" height="{img_height}"/>')
    
    get_preview_image.short_description = 'Превью'


@admin.register(Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    inlines = [PlaceImageInline]


admin.site.site_title = 'Django Places'
admin.site.site_header = 'Django Places'
