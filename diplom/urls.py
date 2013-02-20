# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	(r'ac$', 'diplom.views.predmet_autocomplite'), #обробка автозаповнення предмету
	(r'tch$', 'diplom.views.teacher_autocomplite'), #обробка автозаповнення викладача
	(r'au$', 'diplom.views.audience_autocomplite'), #обробка автозаповнення аудиторiї
	(r'sendsubj$', 'diplom.views.pair_add'), #відправка запиту на додавання заняття
	(r'sendstreamsubj$', 'diplom.views.pair_stream_add'), #відправка запиту на додавання потокового заняття
	(r'getsubjs$', 'diplom.views.group_subjs'), #повертає всі пари для групи
	(r'getsubjsingle$', 'diplom.views.getsubjsingle'), #повертає предмети для певного дня і пари
	(r'getsubjsmodal$', 'diplom.views.getsubjsmodal'), #повертає предмети пари і вводить їх в модальне вікно
	(r'dnd$', 'diplom.views.dnd'), #відправка запиту при перетягуванні заняття
	(r'login$', 'diplom.views.ajax_login'),
	(r'^logout/$', logout, {'template_name': 'login.html'}),
	# Uncomment the admin/doc line below to enable admin documentation:
	# url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

	url(r'^social/', include('social_auth.urls')),

	(r'^about/$', 'diplom.views.about'),
	(r'^rozklad/$', 'diplom.views.rozklad'),
	(r'^rozklad/(.+)/$', 'diplom.views.rozklad_content'),
	(r'^rozklad_teacher/$', 'diplom.views.rozklad_teacher'),
	(r'^rozklad_teacher/(.+)/$', 'diplom.views.rt_content'),
	(r'^forum/$', 'diplom.views.forum'),
	(r'^experimental/$', 'diplom.views.experimental'),

	# Uncomment the next line to enable the admin:
	(r'^admin/', include(admin.site.urls)),
	(r'^rozklad_admin/$', 'diplom.views.rozklad_admin'),
	('^$', 'diplom.views.main'),
)
