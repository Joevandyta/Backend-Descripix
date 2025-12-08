from django.urls import path, include
from . import views

urlpatterns = [

    path('google-login/', views.GoogleSocialAuthView.as_view(), name='google-auth'),
    path('logout/', views.CostumLogoutView.as_view(), name='Logout'),
    path('token-refresh/', views.CostumLoginTokenRefreshView.as_view(), name='token-refresh'),
    path('token-verify/', views.CostumLoginTokenVerifyView.as_view(), name='token-verify'),
    path('user-detail/', views.CostumUserDetailsView.as_view(), name='user-detail'),
    path('user-edit/', views.CostumEditUserView.as_view(), name='user-edit'),
]
