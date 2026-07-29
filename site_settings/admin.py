from django.contrib import admin

from site_settings.models import *



# Register your models here.

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
	list_display = [field.name for field in MenuItem._meta.fields]


@admin.register(RoleMenu)
class RoleMenuAdmin(admin.ModelAdmin):
	list_display = [field.name for field in RoleMenu._meta.fields]


@admin.register(GeneralSetting)
class GeneralSettingAdmin(admin.ModelAdmin):
	list_display = [field.name for field in GeneralSetting._meta.fields]


@admin.register(HomePageSlider)
class HomePageSliderAdmin(admin.ModelAdmin):
	list_display = [field.name for field in HomePageSlider._meta.fields]

@admin.register(ServiceSlider)
class ServiceSliderAdmin(admin.ModelAdmin):
	list_display = [field.name for field in ServiceSlider._meta.fields]

@admin.register(PortfolioCategory)
class PortfolioCategoryAdmin(admin.ModelAdmin):
	list_display = [field.name for field in PortfolioCategory._meta.fields]


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
	list_display = [field.name for field in Portfolio._meta.fields]

@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
	list_display = [field.name for field in About._meta.fields]


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
	list_display = [field.name for field in Client._meta.fields]

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
	list_display = [field.name for field in Testimonial._meta.fields]

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
	list_display = [field.name for field in Gallery._meta.fields]

@admin.register(SisterConcern)
class SisterConcernAdmin(admin.ModelAdmin):
	list_display = [field.name for field in SisterConcern._meta.fields]


@admin.register(SisterConcernImage)
class SisterConcernImageAdmin(admin.ModelAdmin):
	list_display = [field.name for field in SisterConcernImage._meta.fields]


