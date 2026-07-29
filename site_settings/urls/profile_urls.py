
from django.urls import path

from site_settings.views import profile_views as views


urlpatterns = [
	path('api/v1/profile/all/', views.getAllProfile),
    
	path('api/v1/profile/all/wp/', views.getAllProfileWP),

	path('api/v1/profile/<int:pk>', views.getAProfile),

	path('api/v1/profile/create/', views.createProfile),

	path('api/v1/profile/update/<int:pk>', views.updateProfile),
	
	path('api/v1/profile/delete/<int:pk>', views.deleteProfile),
]