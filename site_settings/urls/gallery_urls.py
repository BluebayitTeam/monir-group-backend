
from django.urls import path

from site_settings.views import gallery_views as views


urlpatterns = [
	path('api/v1/gallery/all/', views.getAllGallery),
    
	path('api/v1/gallery/all/wp/', views.getAllGalleryWP),

	path('api/v1/gallery/<int:pk>', views.getAGallery),

	path('api/v1/gallery/create/', views.createGallery),

	path('api/v1/gallery/update/<int:pk>', views.updateGallery),
	
	path('api/v1/gallery/delete/<int:pk>', views.deleteGallery),
]