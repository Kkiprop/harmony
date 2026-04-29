from django.contrib import admin
from .models import Project, Amenity, Enquiry, Unit, GalleryItem
from django.utils.html import format_html


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
	list_display = ('title', 'location', 'progress')
	prepopulated_fields = {'slug': ('title',)}


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
	list_display = ('name',)


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
	list_display = ('name', 'email', 'phone', 'created_at')
	list_filter = ('created_at',)


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
	list_display = ('title', 'unit_type', 'bedrooms', 'bathrooms', 'size_sqm', 'available', 'admin_image')
	list_filter = ('unit_type', 'available')
	search_fields = ('title', 'slug')
	prepopulated_fields = {'slug': ('title',)}

	def admin_image(self, obj):
		# prefer uploaded image_file, fallback to legacy static path
		try:
			if obj.image_file:
				return format_html('<img src="{}" style="height:40px;" />', obj.image_file.url)
		except Exception:
			pass
		if obj.image:
			return format_html('<img src="/static/{}" style="height:40px;" />', obj.image)
		return ''

	admin_image.short_description = 'Image'


@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
	list_display = ('__str__', 'media_type', 'featured', 'order', 'admin_preview')
	list_filter = ('media_type', 'featured')
	search_fields = ('title', 'vimeo_url')

	def admin_preview(self, obj):
		try:
			if obj.media_type == 'image' and obj.image_file:
				return format_html('<img src="{}" style="height:40px;" />', obj.image_file.url)
		except Exception:
			pass
		if obj.media_type == 'video' and obj.vimeo_url:
			return format_html('<a href="{}" target="_blank">Vimeo</a>', obj.vimeo_embed_url())
		return ''

	admin_preview.short_description = 'Preview'
