from django.urls import path
from . import views


app_name = 'post'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('<slug:slug>', views.PostView.as_view(), name='post'),
    path('category/<slug:slug>', views.CategoryPageView.as_view(), name='category'),
    path('category/<slug:slug>/page/<int:page>', views.CategoryPageView.as_view(), name='category'),
    path('tag/<slug:slug>', views.TagPageView.as_view(), name='tag'),
    path('tag/<slug:slug>/page/<int:page>', views.TagPageView.as_view(), name='tag'),
]
