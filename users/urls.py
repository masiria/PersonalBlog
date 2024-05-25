from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register',views.RegisterView.as_view(), name='register'),
    path('activate/<str:uid>/<str:token>', views.ActivateView.as_view(), name='activate')
]