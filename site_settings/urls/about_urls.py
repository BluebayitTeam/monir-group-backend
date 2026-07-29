
from django.urls import path

from site_settings.views import about_views as views


urlpatterns = [
	path('api/v1/about/all/', views.getAllAbout),

	path('api/v1/about/<int:pk>', views.getAAbout),

	path('api/v1/about/create/', views.createAbout),

	path('api/v1/about/update/<int:pk>', views.updateAbout),
	
	path('api/v1/about/delete/<int:pk>', views.deleteAbout),
]