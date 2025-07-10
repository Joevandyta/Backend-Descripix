from django.urls import path
from . import views

urlpatterns = [

    path('save/', views.SaveResultView.as_view(), name='SaveCaptionResult'),
    path('list/', views.GetAllResultView.as_view(), name='GetListCaptions'),
    path('detail/', views.DetailCaptionView.as_view(), name='EditCaption'),
    path('generate/', views.CaptionGenerateView.as_view(), name='GenerateCaption'),
]