
from django.urls import path

from site_settings.views import service_slider_views as views


urlpatterns = [
	path('api/v1/service_slider/all/', views.getAllServiceSlider),

	path('api/v1/service_slider/<int:pk>', views.getAServiceSlider),

	path('api/v1/service_slider/create/', views.createServiceSlider),

	path('api/v1/service_slider/update/<int:pk>', views.updateServiceSlider),
	
	path('api/v1/service_slider/delete/<int:pk>', views.deleteServiceSlider),
]