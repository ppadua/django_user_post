from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^signin$', views.signin),
	url(r'^register$', views.register),
	url(r'^registration$', views.registration),
	url(r'^login$', views.login),
	url(r'^dashboard$', views.user_dashboard),
	url(r'^dashboard/admin$', views.admin_dashboard),
	url(r'^users/new$', views.register),
	url(r'^users/edit/(?P<number>\d+)$', views.admin_edit_user),
	url(r'^users/admin_edit_user$', views.admin_update_user),
	url(r'^users/edit$', views.edit_user),
	url(r'^users/normal_edit_user$', views.normal_edit_user),
	url(r'^users/show/(?P<number>\d+)$', views.show_user),
	url(r'^users/post_message$', views.post_message),
	url(r'^users/post_comment$', views.post_comment),
	url(r'^logoff$', views.logoff),
]