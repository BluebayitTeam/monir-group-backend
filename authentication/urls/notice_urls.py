from django.urls import path

from authentication.views import notice_views as views


urlpatterns = [
	path('api/v1/notice/all/', views.getAllNotice),
 
    path('api/v1/notice/all/without_pagination/', views.getAllNoticeWithoutPagination),

	path('api/v1/notice/<int:pk>', views.getANotice),
    
	path('api/v1/notice/create/', views.createNotice),

	path('api/v1/notice/update/<int:pk>', views.updateNotice),
	
	path('api/v1/notice/delete/<int:pk>', views.deleteNotice),
 
    path('api/v1/notice/search/', views.searchNotice), 
]