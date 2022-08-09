from django.contrib import admin
from django.utils.html import format_html

from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminBase

from places.models import Place, PlaceImage


class PlaceImageInline(SortableInlineAdminMixin, admin.TabularInline):
    model = PlaceImage
    readonly_fields = ['get_preview_image']
    fields = ['image', 'get_preview_image']

    def get_extra(self, request, obj=None, **kwargs):
        extra = 1
        return extra
    
    def get_preview_image(self, obj):        
        return format_html('<img src="{}" style="max-height: 200px;"/>', obj.image.url)
    
    get_preview_image.short_description = 'Превью'


@admin.register(Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    inlines = [PlaceImageInline]


admin.site.site_title = 'Django Places'
admin.site.site_header = 'Django Places'
