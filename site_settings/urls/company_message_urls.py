
from django.urls import path

from site_settings.views import company_message_views as views


urlpatterns = [
	path('api/v1/company_message/all/', views.getAllOurCompanyMessage),

	path('api/v1/company_message/<int:pk>', views.getAOurCompanyMessage),

	path('api/v1/company_message/create/', views.createOurCompanyMessage),

	path('api/v1/company_message/update/<int:pk>', views.updateOurCompanyMessage),
	
	path('api/v1/company_message/delete/<int:pk>', views.deleteOurCompanyMessage),
]