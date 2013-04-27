# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	(r'ac$', 'rozklad.views.predmet_autocomplite'),			#обробка автозаповнення предмету
	(r'tch$', 'rozklad.views.teacher_autocomplite'),		#обробка автозаповнення викладача
	(r'au$', 'rozklad.views.audience_autocomplite'),		#обробка автозаповнення аудиторiї
	(r'gr$', 'rozklad.views.group_autocomplite'),			#обробка автозаповнення групи
	(r'sendsubj$', 'rozklad.views.pair_add'),				#відправка запиту на додавання заняття
	(r'sendstreamsubj$', 'rozklad.views.pair_stream_add'),	#відправка запиту на додавання потокового заняття
	(r'getsubjs$', 'rozklad.views.group_subjs'),			#повертає всі пари для групи
	(r'getsubjsingle$', 'rozklad.views.getsubjsingle'),		#повертає предмети для певного дня і пари
	(r'getsubjsmodal$', 'rozklad.views.getsubjsmodal'),		#повертає предмети пари і вводить їх в модальне вікно
	(r'dnd$', 'rozklad.views.dnd'),							#відправка запиту при перетягуванні заняття
	(r'getaudemp$', 'rozklad.views.getaudemp'),				#зайнятість аудиторій
	(r'getteachemp$', 'rozklad.views.getteachemp'),			#зайнятість викладачів
	(r'getdeptasks$', 'rozklad.views.getdeptasks'),			#завдання кафедр
	(r'adddeptask$', 'rozklad.views.adddeptask'),			#додавання завдання кафедр
	(r'getconformity$', 'rozklad.views.getconformity'),		#відповідність розклада завданню
	(r'delsub$', 'rozklad.views.delsub'),					#видалення занять
	(r'simulate$', 'rozklad.views.simulate'),				#моделювання

	(r'login$', 'diplom.views.ajax_login'),
	(r'^logout/$', logout, {'template_name': 'login.html'}),
	# Uncomment the admin/doc line below to enable admin documentation:
	# url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

	url(r'^social/', include('social_auth.urls')),
	(r'^initialize/$', 'diplom.views.initializebase'),

	(r'^about/$', 'diplom.views.about'),
	(r'^rozklad/$', 'diplom.views.rozklad'),
	(r'^rozklad/(.+)/$', 'diplom.views.rozklad_content'),
	(r'^rozklad_teacher/$', 'diplom.views.rozklad_teacher'),
	(r'^rozklad_teacher/(.+)/$', 'diplom.views.rt_content'),
	(r'^forum/$', 'diplom.views.forum'),
	(r'^experimental/$', 'diplom.views.experimental'),
	(r'^gmaps/$', 'diplom.views.gmaps'),

	# Uncomment the next line to enable the admin:
	(r'^admin/', include(admin.site.urls)),
	(r'^rozklad_admin/$', 'rozklad.views.rozklad_admin'),
	('^$', 'diplom.views.main'),
)
