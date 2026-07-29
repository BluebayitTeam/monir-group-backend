
from django.urls import path

from site_settings.views import sister_concern_views as views


urlpatterns = [
	path('api/v1/sister_concern/all/', views.getAllSisterConcern),

	path('api/v1/sister_concern/<int:pk>', views.getASisterConcern),

	path('api/v1/sister_concern/create/', views.createSisterConcern),

	path('api/v1/sister_concern/update/<int:pk>', views.updateSisterConcern),
	
	path('api/v1/sister_concern/delete/<int:pk>', views.deleteSisterConcern),

]

