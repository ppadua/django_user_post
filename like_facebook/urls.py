from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static

urlpatterns = [
	url(r'^', include('apps.user_dashboard.urls')), 
]	
