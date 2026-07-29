from django.urls import path

from authentication.views import circular_views as views


urlpatterns = [
	path('api/v1/circular/all/', views.getAllCircular),
 
    path('api/v1/circular/without_pagination/all/', views.getAllCircularWithoutPagination),

	path('api/v1/circular/<int:pk>', views.getACircular),
    
	path('api/v1/circular/create/', views.createCircular),

	path('api/v1/circular/update/<int:pk>', views.updateCircular),
	
	path('api/v1/circular/delete/<int:pk>', views.deleteCircular),
 
    path('api/v1/circular/search/', views.searchCircular), 
]