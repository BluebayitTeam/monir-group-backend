
from django.urls import path

from site_settings.views import testimonial_views as views


urlpatterns = [
	path('api/v1/testimonial/all/', views.getAllTestimonial),

	path('api/v1/testimonial/<int:pk>', views.getATestimonial),

	path('api/v1/testimonial/create/', views.createTestimonial),

	path('api/v1/testimonial/update/<int:pk>', views.updateTestimonial),
	
	path('api/v1/testimonial/delete/<int:pk>', views.deleteTestimonial),
]