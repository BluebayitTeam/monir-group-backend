
from django.urls import path

from site_settings.views import portfolio_views as views


urlpatterns = [
	path('api/v1/portfolio/is_portfolio/all/', views.getAllPortfolioForPortfolio),
    
	path('api/v1/portfolio/all/', views.getAllPortfolio),
    
	path('api/v1/portfolio/all/wp/', views.getAllPortfolioWP),
    
	path('api/v1/portfolio/<int:pk>', views.getAPortfolio),

	path('api/v1/portfolio/create/', views.createPortfolio),

	path('api/v1/portfolio/update/<int:pk>', views.updatePortfolio),
	
	path('api/v1/portfolio/delete/<int:pk>', views.deletePortfolio),
]