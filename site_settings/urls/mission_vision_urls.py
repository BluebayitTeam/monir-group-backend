
from django.urls import path

from site_settings.views import mission_vision_views as views


urlpatterns = [
	path('api/v1/mission_vision/all/', views.getAllMissionVission),

	path('api/v1/mission_vision/<int:pk>', views.getAMissionVission),

	path('api/v1/mission_vision/create/', views.createMissionVission),

	path('api/v1/mission_vision/update/<int:pk>', views.updateMissionVission),
	
	path('api/v1/mission_vision/delete/<int:pk>', views.deleteMissionVission),
]