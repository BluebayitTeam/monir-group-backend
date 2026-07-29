
from django.urls import path

from site_settings.views import team_views as views


urlpatterns = [
	path('api/v1/team/all/', views.getAllTeam),

	path('api/v1/team/<int:pk>', views.getATeam),

	path('api/v1/team/create/', views.createTeam),

	path('api/v1/team/update/<int:pk>', views.updateTeam),
	
	path('api/v1/team/delete/<int:pk>', views.deleteTeam),
]