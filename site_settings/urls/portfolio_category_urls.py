
from django.urls import path

from site_settings.views import portfolio_category_views as views


urlpatterns = [
	path('api/v1/portfolio_category/all/', views.getAllPortfolioCategory),

	path('api/v1/portfolio_category/<int:pk>', views.getAPortfolioCategory),

	path('api/v1/portfolio_category/create/', views.createPortfolioCategory),

	path('api/v1/portfolio_category/update/<int:pk>', views.updatePortfolioCategory),
	
	path('api/v1/portfolio_category/delete/<int:pk>', views.deletePortfolioCategory),
]