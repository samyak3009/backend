from django.conf.urls import url
from .views import create_form,login, submit_answer,check_status, test
urlpatterns=[
	url(r'^create_form/$',create_form),
	url(r'^login/$',login),
	url(r'^submit_answer/$',submit_answer),
	url(r'^check_status/$',check_status),
	url(r'^test',test),
]